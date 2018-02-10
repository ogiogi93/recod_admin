"""ww2_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from competition.repository.tournaments import *
from competition.repository.games import *
from competition.repository.teams import *

urlpatterns = [
    url(r'^user_list/edit/(?P<user_id>\d+)/belong_team/$', belong_teams, name='joined_team'),
    url(r'^user_list/edit/(?P<user_id>\d+)/secession_team/(?P<team_id>\d+)/$', secession_team, name='secession_team'),
    url(r'^user_list/edit/join_team/$', join_team, name='join_team'),
    url(r'^team_list/$', team_list, name='team_list'),
    url(r'^team/(?P<user_id>\d+)/create/$', upsert_team, name='create_team'),
    url(r'^team/edit/(?P<team_id>\d+)/$', upsert_team, name='edit_team'),
    url(r'^team/delete/(?P<team_id>\d+)/$', delete_team, name='delete_team'),
    url(r'^team/(?P<team_id>\d+)/participate/$', participate_tournament, name='participate_tournament'),
    url(r'^tournament_list/$', tournament_list, name='tournament_list'),
    url(r'^tournament_list/create/$', upsert_tournament, name='create_tournament'),
    url(r'^tournament_list/edit/(?P<tournament_id>\d+)/$', upsert_tournament, name='edit_tournament'),
    url(r'^participate/(?P<tournament_id>\d+)/(?P<team_id>\d+)/$', refusal_tournament, name='refusal_tournament'),
    url(r'^game/$', game_list, name='game_list'),
    url(r'^game/add/$', upsert_game, name='add_game'),
    url(r'^game/edit/(?P<game_id>\d+)/$', upsert_game, name='edit_game'),
]
