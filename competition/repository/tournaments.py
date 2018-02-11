from django.shortcuts import render, redirect

from competition.api.tournaments import (
    delete_api_tournament,
    refusal_api_participate,
    upsert_api_tournament,
    upsert_api_participate,
)
from competition.infrastructure.tournament import Tournament, Participate
from competition.infrastructure.teams import Team
from competition.forms.tournaments import UpsertTournamentForm, ParticipateTournamentForm


def tournament_list(request):
    """
    大会リストを新しい順番で返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/tournament/tournament_list.html', context={
        'tournaments': Tournament.objects.order_by('-date_start').all()
    })


def upsert_tournament(request, tournament_id=None):
    """
    大会の新規作成・修正を行う
    :param request:
    :param tournament_id:
    :rtype render|redirect:
    """
    if request.method == 'POST':
        # 編集時
        if tournament_id:
            form = UpsertTournamentForm(request.POST, instance=Tournament.objects.get(pk=tournament_id))
            if form.is_valid():
                # Toornament APIにPOSTする
                api_tournament_id = upsert_api_tournament(
                    form.instance, api_tournament_id=Tournament.objects.get(pk=tournament_id).api_tournament_id)
                form.instance.api_tournament_id = api_tournament_id
                form.save()
                return redirect('/competition/tournament_list/')
            return render(request, 'cms/tournament/upsert_tournament.html', context={
                'tournament_id': tournament_id,
                'tournament_api_id': Tournament.objects.get(pk=tournament_id).api_tournament_id,
                'participate_teams': Participate.objects.filter(tournament_id=tournament_id).all(),
                'form': form
            })
        # 新規作成
        form = UpsertTournamentForm(request.POST)
        if form.is_valid():
            # Toornament APIにPOSTする
            api_tournament_id = upsert_api_tournament(form.instance)
            form.instance.api_tournament_id = api_tournament_id
            form.save()
            return redirect('/competition/tournament_list/')
        return render(request, 'cms/tournament/upsert_tournament.html', context={
            'form': form
        })
    return render(request, 'cms/tournament/upsert_tournament.html', context={
        'tournament_id': tournament_id,
        'tournament_api_id': Tournament.objects.get(pk=tournament_id).api_tournament_id,
        'participate_teams': Participate.objects.filter(tournament_id=tournament_id).all(),
        'form': UpsertTournamentForm(
            instance=Tournament.objects.get(pk=tournament_id)) if tournament_id else UpsertTournamentForm()
    })


def participate_tournament(request, team_id):
    """
    大会に参加する
    :param request:
    :param int team_id:
    :rtype render:
    """
    if request.method == 'POST':
        form = ParticipateTournamentForm(request.POST,
                                         initial={'team': Team.objects.get(pk=team_id)})
        # 既に登録済みの大会は除く
        form.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).exclude(participate__team__id=team_id)
        if form.is_valid():
            form.instance.team = Team.objects.get(pk=team_id)
            # Toornament APIの方にも登録しておく
            api_participate_id = upsert_api_participate(form.instance.team,
                                                        api_tournament_id=form.instance.tournament.api_tournament_id)
            form.instance.api_participate_id = api_participate_id
            form.save()
            return redirect('/competition/team/edit/{}/'.format(team_id))
        return render(request, 'cms/tournament/participate_tournament.html', context={
            'form': form
        })
    form = ParticipateTournamentForm()
    # 既に登録済みの大会は除く
    form.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).exclude(participate__team__id=team_id)
    return render(request, 'cms/tournament/participate_tournament.html', context={
        'form': form
    })


def refusal_tournament(request, team_id, tournament_id):
    """
    大会参加を辞退する
    :param request:
    :param int team_id:
    :param int tournament_id:
    :rtype redirect:
    """
    team = Team.objects.get(pk=team_id)
    tournament = Tournament.objects.get(pk=tournament_id)
    if team and tournament:
        participate = Participate.objects.filter(team=team, tournament=tournament).first()
        refusal_api_participate(api_tournament_id=participate.tournament.api_tournament_id,
                                api_participate_id=participate.api_participate_id)
        participate.delete()
    return redirect('/competition/tournament_list/edit/{}/'.format(tournament_id))


def delete_tournament(request, tournament_id):
    """
    大会を削除する
    :param request:
    :param int tournament_id:
    :rtype redirect:
    """
    tournament = Tournament.objects.get(pk=tournament_id)
    if tournament:
        delete_api_tournament(api_tournament_id=tournament.api_tournament_id)
        tournament.delete()
    return redirect('/competition/tournament_list')
