"""動画の投稿者情報を保存する
"""
import random
import time
from functools import lru_cache
from typing import Optional, Iterable, List

from django.utils import timezone

from service_api.models.videos import Author
from video.entity import AuthorEntity
from video.enums import Platform
from video.youtube import V3Channel, V3ChannelEntry
from video.identifier import AuthorIdentifier
from video.repository import NoCacheValueException, LRU_CACHE_MAXSIZE
from video.vo import AuthorVo


def register(platform: Platform, identifier: AuthorIdentifier, is_update: bool = False) -> AuthorEntity:
    """
    :raises ValueError: 動画プラットフォームから指定された投稿者の情報が取得できなかったとき
    """
    author_id = get_author_id(platform, identifier.platform_author_id)
    if is_update is False and author_id:
        return get(author_id)

    v3channel = V3Channel(channel_ids=[identifier.platform_author_id])
    if not v3channel.entries:
        raise ValueError('deleted or restricted channel(id={})'.format(identifier))
    v3 = v3channel.entries[0]
    entity = AuthorEntity(
        author_id=author_id,
        author_vo=_v3channel_entry_to_author_vo(v3)
    )
    entity = save(entity)
    return entity


def save(entity: AuthorEntity, retry: int = 3) -> Optional[AuthorEntity]:
    """動画情報を保存する. author_id 未決の引数を与えた場合, DB の値が反映される"""
    try:
        # validation
        if not entity.author_vo.name:
            raise ValueError('name is empty(platform={}, platform_author_id={})'.format(
                entity.author_vo.platform, entity.author_vo.platform_author_id
            ))

        if entity.author_id:
            author = Author.objects.get(id=entity.author_id)
            if author is None:
                raise ValueError('invalid entity(id={})'.format(entity.author_id))
        else:
            author = Author.objects.filter(
                platform_id=entity.author_vo.platform.value,
                platform_author_id=entity.author_vo.platform_author_id
            ).first()
            if not author:
                author = Author()
                author.created_at = timezone.now()
                author.enabled = True

        author.platform_id = entity.author_vo.platform.value
        author.platform_author_id = entity.author_vo.platform_author_id
        author.name = entity.author_vo.name or '削除済ユーザ'  # これでいいのか感はある
        author.home_url = entity.author_vo.home_url
        author.thumbnail_url = entity.author_vo.thumbnail_url
        author.enabled = entity.author_vo.enabled
        author.view_count = entity.author_vo.view_count
        author.comment_count = entity.author_vo.comment_count
        author.subscriber_count = entity.author_vo.subscriber_count
        author.video_count = entity.author_vo.video_count
        author.modified_at = entity.author_vo.modified_at
        author.updated_at = timezone.now()

        author.save()
        # ID を entity に代入する
        entity = entity._replace(author_id=author.id)
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
def get(author_id: int) -> AuthorEntity:
    author = Author.objects.get(id=author_id)
    if author is None:
        raise ValueError('invalid author id(id={})'.format(author_id))
    return _assemble_author_entity(author)


def gets(author_ids: Iterable[int]) -> List[AuthorEntity]:
    if not author_ids:
        return []

    authors = Author.objects.filter(id__in=author_ids)
    return [_assemble_author_entity(a) for a in authors]


def get_author_id(platform: Platform, platform_author_id: str) -> Optional[int]:
    """unique key を元にして authors テーブルの id を調べる"""
    try:
        return _get_author_id_with_cache(platform, platform_author_id)
    except NoCacheValueException:
        return None


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def _get_author_id_with_cache(platform: Platform, platform_author_id: str) -> int:
    """
    :raises NoCacheValueException: IDが取得できないとき(lru_cacheのキャッシュ対象外の値)
    """
    author = Author.objects.filter(
        platform_id=platform.value,
        platform_author_id=platform_author_id
    ).first()
    # ID が判明したときだけキャッシュする
    if author:
        return author.id
    raise NoCacheValueException(value=None)


def _v3channel_entry_to_author_vo(e: V3ChannelEntry, enabled: bool = True) -> AuthorVo:
    return AuthorVo(
        platform=Platform.YouTube,
        platform_author_id=e.id,
        name=e.title,
        home_url=e.home_url,
        thumbnail_url=e.thumbnail_url,
        enabled=enabled,
        view_count=e.view_count,
        comment_count=e.comment_count,
        subscriber_count=e.subscriber_count,
        video_count=e.video_count,
        modified_at=timezone.now(),
    )


def _assemble_author_entity(author: Author) -> AuthorEntity:
    return AuthorEntity(
        author_id=author.id,
        author_vo=AuthorVo(
            platform=Platform(author.platform_id),
            platform_author_id=author.platform_author_id,
            name=author.name,
            home_url=author.home_url,
            thumbnail_url=author.thumbnail_url,
            enabled=bool(author.enabled),
            view_count=author.view_count,
            comment_count=author.comment_count,
            subscriber_count=author.subscriber_count,
            video_count=author.video_count,
            modified_at=author.modified_at
        )
    )
