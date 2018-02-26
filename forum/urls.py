from django.conf.urls import url

from forum import views


urlpatterns = [
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/edit/(?P<thread_id>\d+)/$', views.upsert_thread, name='edit_thread'),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/delete/(?P<thread_id>\d+)/$', views.delete_thread, name='delete_thread'),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/create/$', views.upsert_thread, name='create_thread'),
    url(r'^(?P<forum_id>\d+)/(?P<topic_id>\d+)/$', views.thread_list, name='thread_list'),
    url(r'^(?P<forum_id>\d+)/edit/(?P<topic_id>\d+)/$', views.upsert_topic, name='edit_topic'),
    url(r'^(?P<forum_id>\d+)/delete/(?P<topic_id>\d+)/$', views.delete_topic, name='delete_topic'),
    url(r'^(?P<forum_id>\d+)/create/$', views.upsert_topic, name='create_topic'),
    url(r'^(?P<forum_id>\d+)/$', views.topic_list, name='topic_list'),
    url(r'^edit/(?P<forum_id>\d+)/$', views.upsert_forum, name='edit_forum'),
    url(r'^delete/(?P<forum_id>\d+)/$', views.delete_forum, name='delete_forum'),
    url(r'^create/$', views.upsert_forum, name='create_forum'),
    url(r'^$', views.forum_list, name='forum_list'),
]
