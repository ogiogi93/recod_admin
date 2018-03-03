from django.conf.urls import url

from team.views import belong_teams, secession_team, join_team, team_list, upsert_team, delete_team

urlpatterns = [
    url(r'^user/edit/(?P<user_id>\d+)/belong_team/$', belong_teams, name='joined_team'),
    url(r'^user/edit/(?P<user_id>\d+)/secession_team/(?P<team_id>\d+)/$', secession_team, name='secession_team'),
    url(r'^user/edit/join_team/$', join_team, name='join_team'),
    url(r'^team/$', team_list, name='team_list'),
    url(r'^team/(?P<user_id>\d+)/create/$', upsert_team, name='create_team'),
    url(r'^team/edit/(?P<team_id>\d+)/$', upsert_team, name='edit_team'),
    url(r'^team/delete/(?P<team_id>\d+)/$', delete_team, name='delete_team'),
]
