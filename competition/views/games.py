from django.shortcuts import render, redirect

from competition.models import Game, Platform
from competition.forms.games import AddGameForm


def game_list(request):
    """
    登録されているゲームリストを返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/competition/game_list.html', context={
        'games': Game.objects.all()
    })


def upsert_game(request):
    """
    ゲームを新規追加または編集をする
    :param request:
    :rtype render:
    """
    if request.method == 'POST':
        form = AddGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/competition//game_list/')
        return render(request, 'cms/competition/add_new_game.html', context={
            'form': form
        })
    return render(request, 'cms/competition/add_new_game.html', context={
        'form': AddGameForm()
    })
