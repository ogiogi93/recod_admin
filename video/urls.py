from django.conf.urls import url

from video.views import video_list, upsert_video, upsert_video_attribute


urlpatterns = [
    url(r'^(?P<video_id>\d+)/$', upsert_video_attribute, name='edit_video_attribute'),
    url(r'^crawl/$', upsert_video, name='crawl_video'),
    url(r'^$', video_list, name='video_list'),
]
