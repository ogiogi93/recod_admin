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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from account.views import *
from cms.views import *
from team.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', top, name='top'),
    url(r'^user_list/$', user_list, name='user_list'),
    url(r'^user_list/add/$', add_user, name='add_user'),
    url(r'^user_list/edit/(?P<user_id>\d+)/$', edit_user, name='edit_user'),
    url(r'^user_list/edit/(?P<user_id>\d+)/joined_team/$', joined_teams, name='joined_team'),
    url(r'^user_list/edit/(?P<user_id>\d+)/secession_team/(?P<team_id>\d+)/$', secession_team, name='secession_team'),
    url(r'^user_list/edit/join_team/$', join_team, name='join_team'),
    url(r'^user_list/delete/(?P<user_id>\d+)/$', delete_user, name='delete_user'),
    url(r'^team_list/$', team_list, name='team_list'),
    url(r'^team/(?P<user_id>\d+)/create/$', create_team_page, name='create_team'),
    url(r'^team/edit/(?P<team_id>\d+)/$', edit_team, name='edit_team'),
    url(r'^team/delete/(?P<team_id>\d+)/$', delete_team, name='delete_team'),
]
