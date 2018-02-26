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
from django.conf.urls import include, url
from django.shortcuts import render
from django.urls import path

import account.urls as account_urls
import article.urls as article_urls
import competition.urls.games as games
import competition.urls.matches as matches
import competition.urls.teams as teams
import competition.urls.tournaments as tournaments
import forum.urls as forum_urls


def top(request):
    return render(request, 'cms/index.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', top, name='top'),
    url(r'^user/', include(account_urls)),
    url(r'^article/', include(article_urls)),
    url(r'^competition/', include(games)),
    url(r'^competition/', include(matches)),
    url(r'^competition/', include(teams)),
    url(r'^competition/', include(tournaments)),
    url(r'^forum/', include(forum_urls)),
]
