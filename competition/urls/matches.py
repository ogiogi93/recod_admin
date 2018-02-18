from django.conf.urls import url

from competition.repository import matches

urlpatterns = [
    url(r'^tournament/(?P<match_id>\d+)/$', matches.update_match, name='update_match'),
    url(r'^tournament/(?P<match_id>\d+)/update/$', matches.update_match, name='update_match_team'),
]
