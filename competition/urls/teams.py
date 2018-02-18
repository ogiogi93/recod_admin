from django.conf.urls import url

from competition.repository import teams

urlpatterns = [
    url(r'^user/edit/(?P<user_id>\d+)/belong_team/$', teams.belong_teams, name='joined_team'),
    url(r'^user/edit/(?P<user_id>\d+)/secession_team/(?P<team_id>\d+)/$', teams.secession_team, name='secession_team'),
    url(r'^user/edit/join_team/$', teams.join_team, name='join_team'),
    url(r'^team/$', teams.team_list, name='team_list'),
    url(r'^team/(?P<user_id>\d+)/create/$', teams.upsert_team, name='create_team'),
    url(r'^team/edit/(?P<team_id>\d+)/$', teams.upsert_team, name='edit_team'),
    url(r'^team/delete/(?P<team_id>\d+)/$', teams.delete_team, name='delete_team'),
]
