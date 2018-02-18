from django.conf.urls import url

from competition.repository import tournaments


urlpatterns = [
    url(r'^team/(?P<team_id>\d+)/participate/$', tournaments.participate_tournament, name='participate_tournament'),
    url(r'^tournament/$', tournaments.tournament_list, name='tournament_list'),
    url(r'^tournament/create/$', tournaments.upsert_tournament, name='create_tournament'),
    url(r'^tournament/edit/(?P<tournament_id>\d+)/$', tournaments.upsert_tournament, name='edit_tournament'),
    url(r'^tournament/delete/(?P<tournament_id>\d+)/$', tournaments.delete_tournament, name='delete_tournament'),
    url(r'^tournament/update/(?P<tournament_id>\d+)/match/$',
        tournaments.get_and_upsert_matches, name='update_tournament_match'),
    url(r'^tournament/participate/(?P<tournament_id>\d+)/(?P<team_id>\d+)/$',
        tournaments.refusal_tournament, name='refusal_tournament')
]
