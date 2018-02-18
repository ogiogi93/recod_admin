from django.conf.urls import url

from competition.repository import games


urlpatterns = [
    url(r'^game/(?P<game_id>\d+)/map/(?P<map_id>\d+)/$', games.upsert_map, name='edit_map'),
    url(r'^game/(?P<game_id>\d+)/map/add/$', games.upsert_map, name='add_map'),
    url(r'^game/edit/(?P<game_id>\d+)/$', games.upsert_game, name='edit_game'),
    url(r'^game/add/$', games.upsert_game, name='add_game'),
    url(r'^game/$', games.game_list, name='game_list'),
]
