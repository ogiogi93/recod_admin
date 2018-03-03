from django.shortcuts import render, redirect

from service_api.models.disciplines import Game, Map
from competition.forms.games import UpsertGameForm, UpsertMapForm


def game_list(request):
    """
    登録されているゲームリストを返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/game/game_list.html', context={
        'games': Game.objects.all()
    })


def upsert_game(request, game_id=None):
    """
    ゲームを新規追加または編集をする
    :param request:
    :param int game_id:
    :rtype render:
    """
    if request.method == 'POST':
        # 編集時
        if game_id:
            form = UpsertGameForm(request.POST, instance=Game.objects.get(pk=game_id))
            if form.is_valid():
                form.save()
                return redirect('/competition/game/')
            return render(request, 'cms/game/upsert_game.html', context={
                'form': form,
                'game_id': game_id,
                'maps': Map.objects.filter(game_id=game_id)
            })
        # 新規追加
        form = UpsertGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/competition/game/')
        return render(request, 'cms/game/upsert_game.html', context={
            'form': form,
            'game_id': game_id,
            'maps': Map.objects.filter(game_id=game_id)
        })
    return render(request, 'cms/game/upsert_game.html', context={
        'form': UpsertGameForm(instance=Game.objects.get(pk=game_id)) if game_id else UpsertGameForm(),
        'game_id': game_id,
        'maps': Map.objects.filter(game_id=game_id) if game_id else None
    })


def upsert_map(request, game_id, map_id=None):
    """
    マップを新規追加または編集する
    :param request:
    :param int game_id:
    :param int|None map_id:
    :rtype render:
    """
    if request.method == 'POST':
        form = UpsertMapForm(request.POST)
        form.instance.game = Game.objects.get(pk=game_id)
        if form.is_valid():
            form.save()
            return redirect('/competition/game/edit/{}'.format(game_id))
        return render(request, 'cms/game/upsert_map.html', context={
            'form': form,
            'game_id': game_id,
            'map_id': map_id
        })
    return render(request, 'cms/game/upsert_map.html', context={
        'form': UpsertMapForm(instance=Map.objects.get(pk=map_id)) if map_id else UpsertMapForm(),
        'game_id': game_id,
        'map_id': map_id if map_id else None
    })
