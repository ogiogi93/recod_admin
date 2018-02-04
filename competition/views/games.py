from django.shortcuts import render, redirect

from competition.models import Game
from competition.forms.games import UpsertGameForm


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
                'form': form
            })
        # 新規追加
        form = UpsertGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/competition/game/')
        return render(request, 'cms/game/upsert_game.html', context={
            'form': form
        })
    return render(request, 'cms/game/upsert_game.html', context={
        'form': UpsertGameForm(instance=Game.objects.get(pk=game_id)) if game_id else UpsertGameForm()
    })
