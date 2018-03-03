from video.repository.video import register
from video.identifier import YouTubeVideoIdentifier


def upsert_video(platform_video_id):
    register(identifier=YouTubeVideoIdentifier(platform_video_id))
