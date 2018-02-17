from django.conf.urls import url

from competition.repository import games


urlpatterns = [
    url(r'^game/$', games.game_list, name='game_list'),
    url(r'^game/add/$', games.upsert_game, name='add_game'),
    url(r'^game/edit/(?P<game_id>\d+)/$', games.upsert_game, name='edit_game'),
]
