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

from competition.views.competitions import *
from competition.views.games import *
from competition.views.teams import *

urlpatterns = [
    url(r'^user_list/edit/(?P<user_id>\d+)/joined_team/$', joined_teams, name='joined_team'),
    url(r'^user_list/edit/(?P<user_id>\d+)/secession_team/(?P<team_id>\d+)/$', secession_team, name='secession_team'),
    url(r'^user_list/edit/join_team/$', join_team, name='join_team'),
    url(r'^team_list/$', team_list, name='team_list'),
    url(r'^team/(?P<user_id>\d+)/create/$', create_team_page, name='create_team'),
    url(r'^team/edit/(?P<team_id>\d+)/$', edit_team, name='edit_team'),
    url(r'^team/delete/(?P<team_id>\d+)/$', delete_team, name='delete_team'),
    url(r'^competition_list/$', competition, name='competition_list'),
    url(r'^competition_list/create/$', create_competition, name='create_competition'),
    url(r'^game_list/$', game_list, name='game_list'),
    url(r'^game_list/add/$', upsert_game, name='upsert_game'),
]
