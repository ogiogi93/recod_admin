from typing import NamedTuple, Optional

from video.vo import AuthorVo, VideoVo


class VideoEntity(NamedTuple):
    video_id: Optional[int]
    author_id: Optional[int]
    video_vo: VideoVo
    author_vo: AuthorVo


class AuthorEntity(NamedTuple):
    author_id: Optional[int]
    author_vo: AuthorVo
