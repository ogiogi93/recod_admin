from django.conf.urls import url

from match.views import update_match

urlpatterns = [
    url(r'^tournament/(?P<match_id>\d+)/$', update_match, name='update_match'),
    url(r'^tournament/(?P<match_id>\d+)/update/$', update_match, name='update_match_team'),
]
