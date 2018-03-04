import datetime
import json
import random
import time
from abc import ABC, abstractmethod
from typing import List, Optional, Iterable

import dateutil.parser
import isodate
from requests import Response, RequestException

from recod_admin.static_settings import STATIC_SETTINGS
from video import httpclient


class _ApiBase(ABC):
    """v3 API にリクエストを送る処理の基底クラス"""

    def __init__(self) -> None:
        self._response = None

    @property
    @abstractmethod
    def endpoint_url(self) -> str:
        pass

    @property
    def response(self) -> Response:
        if not isinstance(self._response, Response):
            try:
                self._response = httpclient.get(self.endpoint_url)
            except RequestException:
                # 数秒待って 1 回だけ retry する
                time.sleep(1 + round(random.random() * 2, 2))
                self._response = httpclient.get(self.endpoint_url)
        return self._response


class V3VideoEntry:
    def __init__(self, data: dict) -> None:
        """
        :param dict data: v3 API のレスポンスの item の各要素
        """
        self._data = data

    @property
    def id(self) -> str:
        return self._data['id']

    @property
    def title(self) -> str:
        snippet = self._data['snippet']
        return snippet.get('localized', {}).get('title') or snippet['title']

    @property
    def channel_id(self) -> str:
        return self._data['snippet']['channelId']

    @property
    def description(self) -> str:
        snippet = self._data['snippet']
        return snippet.get('localized', {}).get('description') or snippet['description']

    @property
    def thumbnail_url(self) -> str:
        """API で得られた画像 URL について, 高解像度なものから優先して返す
        投稿後すぐの動画は高解像度のサムネイルが生成されていないことがある.
        medium, maxres 以外は上下に黒帯が入ることが多いのでサムネ候補として優先度を下げる.
        maxres(1280x720) => standard(640x480) => high(480x360) => medium(320x180) => default(120x90)
        :return: サムネイルのURL. サムネイルがない場合は空文字列を返す
        """
        snippet = self._data['snippet']
        if 'thumbnails' not in snippet:
            # アップロード失敗動画はサムネイルが生成されず, api に key も入ってない
            return ''
        ts = snippet['thumbnails']
        return (ts.get('medium') or ts.get('standard') or ts.get('high') or {}).get('url') or ''

    @property
    def enabled(self) -> bool:
        # サムネが空の動画は使用不可
        if not self.thumbnail_url:
            return False

        # アップロードが完了してない or 貼り付け不可な動画は使用不可にする
        status = self._data['status']
        if status['uploadStatus'] != 'processed' or status['embeddable'] is not True:
            return False

        content_details = self._data.get('contentDetails')
        # 削除された動画は contentDetails が入っていないことがある
        if content_details is None:
            return False

        # 視聴地域が限定されている動画は WebView で再生不能なことがある
        region_restriction = content_details.get('regionRestriction')
        if region_restriction:
            return False

        # 年齢制限がかかっている動画は WebView で再生不能なことがある
        content_rating = content_details.get('contentRating', False)
        if content_rating:
            return False

        # 使用不可の条件を満たしていない動画は使用可
        return True

    @property
    def published_at(self) -> Optional[datetime.datetime]:
        snippet = self._data['snippet']
        if 'publishedAt' in snippet:
            return dateutil.parser.parse(snippet['publishedAt'])
        else:
            return None

    @property
    def view_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics['viewCount']) if 'viewCount' in statistics else None

    @property
    def like_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics['likeCount']) if 'likeCount' in statistics else None

    @property
    def dislike_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics['dislikeCount']) if 'dislikeCount' in statistics else None

    @property
    def favorite_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics['favoriteCount']) if 'favoriteCount' in statistics else None

    @property
    def comment_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics['commentCount']) if 'commentCount' in statistics else None

    @property
    def duration(self) -> Optional[int]:
        content_details = self._data.get('contentDetails', {})
        if 'duration' in content_details:
            return int(isodate.parse_duration(content_details['duration']).total_seconds())
        else:
            return None

    @property
    def channel_title(self) -> str:
        snippet = self._data['snippet']
        return snippet.get('channelTitle') or ''

    @property
    def tags(self) -> List[str]:
        snippet = self._data['snippet']
        return snippet['tags'] if 'tags' in snippet else []

    @property
    def category_id(self) -> Optional[int]:
        snippet = self._data['snippet']
        return int(snippet['categoryId']) if 'categoryId' in snippet else None

    @property
    def original_url(self) -> str:
        return 'https://www.youtube.com/watch?v={}'.format(self.id)


class V3Video(_ApiBase):
    """v3 API で動画情報を取得する"""

    def __init__(self, video_ids: Iterable[str]) -> None:
        super().__init__()
        self.video_ids = set(video_ids)
        self._entries = None
        self._entry_map = None

    @property
    def endpoint_url(self) -> str:
        # see: https://developers.google.com/youtube/v3/docs/videos?hl=ja
        # 取得要素の絞り込みを行わえば 1 リクエストあたりのクォータ数を減らすことができる
        return (
            'https://www.googleapis.com/youtube/v3/videos'
            '?id={id}&key={key}'
            '&part=status,statistics,snippet,contentDetails'
            '&hl=ja'
        ).format(id=','.join(self.video_ids), key=STATIC_SETTINGS['YOUTUBE_API_KEY'])

    def get_entry(self, video_id: str) -> Optional[V3VideoEntry]:
        if not isinstance(self._entry_map, dict):
            self._entry_map = {e.id: e for e in self.entries}
        return self._entry_map.get(video_id)

    @property
    def entries(self) -> List[V3VideoEntry]:
        if not isinstance(self._entries, list):
            self.response.raise_for_status()
            items = json.loads(self.response.content.decode('utf-8'))['items']
            self._entries = [V3VideoEntry(item) for item in items]
        return self._entries


class V3ChannelEntry:
    def __init__(self, data: dict) -> None:
        """
        :param dict data: v3 API のレスポンスの item の各要素
        """
        self._data = data

    @property
    def id(self) -> str:
        return self._data['id']

    @property
    def title(self) -> str:
        snippet = self._data['snippet']
        return snippet.get('localized', {}).get('title') or snippet['title']

    @property
    def thumbnail_url(self) -> str:
        """API で得られた画像 URL について, 高解像度なものから優先して返す
        :return: サムネイルのURL. サムネイルがない場合は空文字列を返す
        """
        snippet = self._data['snippet']
        if 'thumbnails' not in snippet:
            # アップロード失敗動画はサムネイルが生成されず, api に key も入ってない
            return ''
        ts = snippet['thumbnails']
        return (ts.get('high') or ts.get('medium') or ts.get('default') or {}).get('url') or ''

    @property
    def view_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics['viewCount']) if 'viewCount' in statistics else None

    @property
    def comment_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics['commentCount']) if 'commentCount' in statistics else None

    @property
    def subscriber_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})

        if len(statistics) <= 0 or statistics.get('hiddenSubscriberCount', False):
            return None
        return int(statistics.get('subscriberCount', 0))

    @property
    def video_count(self) -> Optional[int]:
        statistics = self._data.get('statistics', {})
        return int(statistics.get('videoCount', 0)) if 'videoCount' in statistics else None

    @property
    def home_url(self) -> str:
        return 'https://www.youtube.com/channel/{}'.format(self.id)


class V3Channel(_ApiBase):
    """v3 API でチャンネル情報を取得する"""

    def __init__(self, channel_ids: Iterable[str]) -> None:
        super().__init__()
        self.channel_ids = set(channel_ids)
        self._entries = None
        self._entry_map = None

    def get_entry(self, channel_id: str) -> Optional[V3ChannelEntry]:
        if not isinstance(self._entry_map, dict):
            self._entry_map = {e.id: e for e in self.entries}
        return self._entry_map.get(channel_id)

    @property
    def endpoint_url(self) -> str:
        # see: https://developers.google.com/youtube/v3/docs/channels?hl=ja
        return (
            'https://www.googleapis.com/youtube/v3/channels'
            '?part=id,snippet,statistics'
            '&id={id}&key={key}'
            '&hl=ja'
        ).format(id=','.join(self.channel_ids), key=STATIC_SETTINGS['YOUTUBE_API_KEY'])

    @property
    def entries(self) -> List[V3ChannelEntry]:
        if not isinstance(self._entries, list):
            self.response.raise_for_status()
            items = json.loads(self.response.content.decode('utf-8'))['items']
            self._entries = [V3ChannelEntry(item) for item in items]
        return self._entries
