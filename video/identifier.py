from abc import ABC, abstractmethod
from typing import Any


class VideoIdentifier(ABC):
    """Platform毎に動画を識別するための最小要素を示すクラスの基底クラス"""

    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def id(self) -> Any:
        """プラットフォーム毎に固有の動画の識別子を返す"""
        pass

    @property
    @abstractmethod
    def platform_video_id(self) -> str:
        pass

    def __eq__(self, other) -> bool:
        self_class = self.__class__
        other_class = other.__class__
        return self_class == other_class and self.id == other.id


class AuthorIdentifier(ABC):
    """Platform毎に投稿者(ないし投稿先サイト)を識別するための最小要素を示すクラスの基底クラス"""

    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def id(self) -> Any:
        """プラットフォーム毎に固有の動画の識別子を返す"""
        pass

    @property
    @abstractmethod
    def platform_author_id(self) -> str:
        pass

    def __eq__(self, other) -> bool:
        self_class = self.__class__
        other_class = other.__class__
        return self_class == other_class and self.id == other.id

    def __repr__(self) -> str:
        return str('{}: {}'.format(self.__class__.__name__, self.id))


class YouTubeVideoIdentifier(VideoIdentifier):
    """YouTubeの動画を識別するための必要最小の情報"""

    def __init__(self, video_id: str) -> None:
        super().__init__()
        self.video_id = video_id

    @property
    def platform_video_id(self) -> str:
        """alias of self.video_id"""
        return self.video_id

    @property
    def id(self) -> str:
        return self.platform_video_id


class YouTubeAuthorIdentifier(AuthorIdentifier):
    """YouTubeの動画を識別するための必要最小の情報"""

    def __init__(self, author_id: str) -> None:
        super().__init__()
        self.author_id = author_id

    @property
    def id(self) -> str:
        return self.platform_author_id

    @property
    def platform_author_id(self) -> str:
        """alias of self.author_id"""
        return self.author_id
