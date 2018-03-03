from django.conf.urls import url

from game.views import upsert_game, upsert_map, game_list


urlpatterns = [
    url(r'^game/(?P<game_id>\d+)/map/(?P<map_id>\d+)/$', upsert_map, name='edit_map'),
    url(r'^game/(?P<game_id>\d+)/map/add/$', upsert_map, name='add_map'),
    url(r'^game/edit/(?P<game_id>\d+)/$', upsert_game, name='edit_game'),
    url(r'^game/add/$', upsert_game, name='add_game'),
    url(r'^game/$', game_list, name='game_list'),
]
