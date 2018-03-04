from django.conf.urls import url

from article import views


urlpatterns = [
    url(r'^edit/(?P<article_id>\d+)/$', views.upsert_article, name='edit_article'),
    url(r'^delete/(?P<article_id>\d+)/$', views.delete_article, name='delete_article'),
    url(r'^publish/$', views.upsert_article, name='publish_article'),
    url(r'^$', views.article_list, name='article_list'),
]
