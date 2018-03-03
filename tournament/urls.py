from django.conf.urls import url

from tournament.views import (
    participate_tournament, tournament_list,
    get_and_upsert_matches, refusal_tournament,
    upsert_tournament, delete_tournament
)


urlpatterns = [
    url(r'^team/(?P<team_id>\d+)/participate/$', participate_tournament, name='participate_tournament'),
    url(r'^tournament/$', tournament_list, name='tournament_list'),
    url(r'^tournament/create/$', upsert_tournament, name='create_tournament'),
    url(r'^tournament/edit/(?P<tournament_id>\d+)/$', upsert_tournament, name='edit_tournament'),
    url(r'^tournament/delete/(?P<tournament_id>\d+)/$', delete_tournament, name='delete_tournament'),
    url(r'^tournament/update/(?P<tournament_id>\d+)/match/$',
        get_and_upsert_matches, name='update_tournament_match'),
    url(r'^tournament/participate/(?P<tournament_id>\d+)/(?P<team_id>\d+)/$',
        refusal_tournament, name='refusal_tournament')
]
