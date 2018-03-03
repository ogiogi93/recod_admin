"""動画IDとEntityの変換処理およびEntityのCRUDを行う
"""
import random
import time
from functools import lru_cache
from typing import Optional  # noqa
from logging import getLogger

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from video.youtube import V3Video, V3VideoEntry
from service_api.models.videos import Video, VideoText
from video.entity import VideoEntity, AuthorEntity
from video.enums import Platform
from video.repository import author, LRU_CACHE_MAXSIZE, NoCacheValueException
from video.vo import VideoVo
from video.identifier import VideoIdentifier, YouTubeAuthorIdentifier

logger = getLogger(__name__)


def register(identifier: VideoIdentifier) -> Optional[VideoEntity]:
    """
    :raises ValueError: 動画プラットフォームから指定された動画の情報が取得できなかったとき
    """
    v3video = V3Video(video_ids=[identifier.platform_video_id])
    if not v3video.entries:
        logger.warning('deleted or restricted youtube video id={}'.format(identifier.platform_video_id))
        return
    return _register_v3video(v3video.entries[0], is_update=True)


def _register_v3video(v3entry: V3VideoEntry, is_update: bool = True) -> Optional[VideoEntity]:
    if is_update is False:
        video_id = get_video_id(Platform.YouTube, v3entry.id)
        if video_id:
            return get(video_id)
    author_entity = author.register(Platform.YouTube, YouTubeAuthorIdentifier(v3entry.channel_id), is_update=is_update)
    entity = VideoEntity(
        video_id=None,
        video_vo=_v3video_entry_to_video_vo(v3entry),
        author_id=author_entity.author_id,
        author_vo=author_entity.author_vo
    )
    entity = save(entity)
    return entity


def register_video_vo(vo: VideoVo, is_update: bool = True) -> VideoEntity:
    """VideoVoを直接登録する. author_idは必須.
    :raises ValueError: 動画プラットフォームから指定された動画の情報が取得できなかったとき
    """
    if not vo.platform_author_id:
        raise ValueError('platform_author_id is empty')

    if is_update is False:
        video_id = get_video_id(vo.platform, vo.platform_video_id)
        if video_id:
            return get(video_id)
    author_id = author.get_author_id(platform=vo.platform, platform_author_id=vo.platform_author_id)
    if not author_id:
        raise ValueError('author_id is empty')
    author_entity = author.get(author_id)
    # validate
    if vo.platform != author_entity.author_vo.platform:
        raise ValueError('invalid platform(arg platform={}, db={})'.format(
            vo.platform,
            author_entity.author_vo.platform
        ))
    entity = VideoEntity(
        video_id=None,
        video_vo=vo,
        author_id=author_id,
        author_vo=author_entity.author_vo
    )
    save(entity)
    return entity


def save(entity: VideoEntity, retry: int = 3) -> Optional[VideoEntity]:
    """動画情報を保存する. author_id, video_id 未決の引数を与えた場合, DB の値が反映される"""
    if entity.video_id is None:
        entity = entity._replace(video_id=get_video_id(entity.video_vo.platform, entity.video_vo.platform_video_id))

    try:
        if entity.author_id is None:
            author_id = author.get_author_id(entity.author_vo.platform, entity.author_vo.platform_author_id)
            if author_id is None:
                raise ValueError('invalid or unsaved author(platform={}, platform_author_id={})'.format(
                    entity.author_vo.platform, entity.author_vo.platform_author_id))
            # ID を entity に代入する
            entity = entity._replace(author_id=author_id)

        if entity.video_id:
            video = Video.objects.get(id=entity.video_id)
            if video is None:
                raise ValueError('invalid entity(id={})'.format(entity.video_id))
        else:
            video = Video()
            video.created_at = timezone.now()
            video.enabled = True

        video.platform_id = entity.video_vo.platform.value
        video.platform_video_id = entity.video_vo.platform_video_id
        video.platform_category_id = entity.video_vo.platform_category_id
        video.author_id = entity.author_id
        if video.title == video.original_title:
            # タイトルがリライト(加工)されていないときのみ保存(更新)する
            video.title = entity.video_vo.title
        video.original_title = entity.video_vo.original_title
        video.thumbnail_url = entity.video_vo.thumbnail_url
        video.mp4_url = entity.video_vo.mp4_url
        # 削除済のものは削除済のままにしておく (True のときだけ上書き判定を行う)
        if video.enabled:
            video.enabled = entity.video_vo.enabled
        video.original_url = entity.video_vo.original_url
        video.duration = entity.video_vo.duration
        video.width = entity.video_vo.width
        video.height = entity.video_vo.height
        video.view_count = entity.video_vo.view_count
        video.like_count = entity.video_vo.like_count
        video.dislike_count = entity.video_vo.dislike_count
        video.favorite_count = entity.video_vo.favorite_count
        video.comment_count = entity.video_vo.comment_count
        video.modified_at = entity.video_vo.modified_at
        video.published_at = entity.video_vo.published_at
        video.updated_at = timezone.now()
        video.save()

        # ID を entity に代入する
        entity = entity._replace(video_id=video.id)

        try:
            video_text = VideoText.objects.get(video_id=entity.video_id)
        except ObjectDoesNotExist:
            video_text = VideoText()
            video_text.video_id = entity.video_id
        # update_at はないので created_at を更新して delete - insert を装う
        video_text.created_at = timezone.now()
        video_text.text = entity.video_vo.text
        try:
            # utf8mb4でもエラーがでる絵文字が存在する
            video_text.save()
        except:
            video_text.text = ''
            video_text.save()

        # 正常終了
        retry = 0
        return entity

    except Exception:
        if retry <= 0:
            raise

    if retry > 0:
        time.sleep(round(random.random(), 2))
        save(entity, retry - 1)
        return


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def get(video_id: int) -> VideoEntity:
    video = Video.objects.filter(id=video_id).first()
    if video is None:
        raise ValueError('invalid video id(id={})'.format(video_id))
    author_entity = author.get(video.author_id)
    return _assemble_video_entity(
        video=video,
        author_entity=author_entity,
        video_text=None,
    )


def get_video_id(platform: Platform, platform_video_id: str) -> Optional[int]:
    """unique key を元にして videos テーブルの id を調べる"""
    try:
        return _get_video_id_with_cache(platform, platform_video_id)
    except NoCacheValueException:
        return None


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def _get_video_id_with_cache(platform: Platform, platform_video_id: str) -> int:
    """
    :raises NoCacheValueException: IDが取得できないとき(lru_cacheのキャッシュ対象外の値)
    """
    video = Video.objects.filter(
        platform_id=platform.value,
        platform_video_id=platform_video_id
    ).first()
    # ID が判明したときだけキャッシュする
    if video:
        return video.id
    raise NoCacheValueException(value=None)


def _v3video_entry_to_video_vo(e: V3VideoEntry) -> VideoVo:
    return VideoVo(
        platform=Platform.YouTube,
        platform_video_id=e.id,
        platform_category_id=e.category_id,
        platform_author_id=e.channel_id,
        title=e.title,
        original_title=e.title,
        thumbnail_url=e.thumbnail_url,
        mp4_url=None,
        text=e.description,
        enabled=e.enabled,
        original_url=e.original_url,
        duration=e.duration,
        width=640,  # 固定のはず
        height=360,  # 固定のはず
        view_count=e.view_count,
        like_count=e.like_count,
        dislike_count=e.dislike_count,
        favorite_count=e.favorite_count,
        comment_count=e.comment_count,
        modified_at=e.published_at,  # published_atと同じ
        published_at=e.published_at,
    )


def _assemble_video_entity(
        video: Video,
        author_entity: AuthorEntity,
        video_text: Optional[VideoText]) -> VideoEntity:
    """引数のオブジェクト群からVideoEntityを組み立てる"""
    return VideoEntity(
        video_id=video.pk,
        video_vo=VideoVo(
            platform=Platform(video.platform_id),
            platform_video_id=video.platform_video_id,
            platform_category_id=video.platform_category_id,
            platform_author_id=author_entity.author_vo.platform_author_id,
            title=video.title,
            original_title=video.title,
            thumbnail_url=video.thumbnail_url,
            mp4_url=video.mp4_url,
            text=video_text.text if video_text else '',
            enabled=bool(video.enabled),
            original_url=video.original_url,
            duration=video.duration,
            width=video.width,
            height=video.height,
            view_count=video.view_count,
            like_count=video.like_count,
            dislike_count=video.dislike_count,
            favorite_count=video.favorite_count,
            comment_count=video.comment_count,
            modified_at=video.modified_at,
            published_at=video.published_at,
        ),
        author_id=author_entity.author_id,
        author_vo=author_entity.author_vo
    )
