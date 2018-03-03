import datetime
from typing import Optional, Sequence, NamedTuple
from video.enums import Platform


class VideoVo(NamedTuple):
    platform: Platform
    platform_video_id: str
    platform_category_id: Optional[int]
    platform_author_id: str
    title: str
    original_title: str
    thumbnail_url: Optional[str]
    mp4_url: Optional[str]
    text: Optional[str]
    enabled: bool
    original_url: Optional[str]
    duration: Optional[int]
    width: Optional[int]
    height: Optional[int]
    view_count: Optional[int]
    like_count: Optional[int]
    dislike_count: Optional[int]
    favorite_count: Optional[int]
    comment_count: Optional[int]
    modified_at: datetime.datetime
    published_at: datetime.datetime


class AuthorVo(NamedTuple):
    platform: Platform
    platform_author_id: str
    name: str
    home_url: Optional[str]
    thumbnail_url: Optional[str]
    enabled: bool
    view_count: Optional[int]
    comment_count: Optional[int]
    subscriber_count: Optional[int]
    video_count: Optional[int]
    modified_at: datetime.datetime
