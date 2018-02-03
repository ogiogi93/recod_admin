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

from account.views import *

urlpatterns = [
    url(r'^user_list/$', user_list, name='user_list'),
    url(r'^user_list/add/$', add_user, name='add_user'),
    url(r'^user_list/edit/(?P<user_id>\d+)/$', edit_user, name='edit_user'),
    url(r'^user_list/delete/(?P<user_id>\d+)/$', delete_user, name='delete_user'),
]
