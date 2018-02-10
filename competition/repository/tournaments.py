from django.shortcuts import render, redirect

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
        'tournaments': Tournament.objects.order_by('start_date').all()
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
                form.save()
                return redirect('/tournament/tournament_list/')
            return render(request, 'cms/tournament/upsert_tournament.html', context={
                'tournament_id': tournament_id,
                'participate_teams': Participate.objects.filter(tournament_id=tournament_id).all(),
                'form': form
            })
        # 新規作成
        form = UpsertTournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tournament/tournament_list/')
        return render(request, 'cms/tournament/upsert_tournament.html', context={
            'form': form
        })
    return render(request, 'cms/tournament/upsert_tournament.html', context={
        'tournament_id': tournament_id,
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
        form = ParticipateTournamentForm(request.POST, initial={'team': Team.objects.get(pk=team_id)})
        if form.is_valid():
            form.instance.team = Team.objects.get(pk=team_id)
            form.save()
            return redirect('/tournament/team/edit/{}/'.format(team_id))
        return render(request, 'cms/tournament/participate_tournament.html', context={
            'form': form
        })
    return render(request, 'cms/tournament/participate_tournament.html', context={
        'form': ParticipateTournamentForm()
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
        participate = Participate.objects.filter(team=team, tournament=tournament)
        participate.delete()
    return redirect('tournament/tournament_list/edit/{}/'.format(tournament_id))
