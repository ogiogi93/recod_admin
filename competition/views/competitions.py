from django.shortcuts import render, redirect

from competition.models import Competition, Participate, Team
from competition.forms.competitions import UpsertCompetitionForm, ParticipateCompetitionForm


def competition_list(request):
    """
    大会リストを新しい順番で返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/competition/competition_list.html', context={
        'competitions': Competition.objects.order_by('start_date').all()
    })


def upsert_competition(request, competition_id=None):
    """
    大会の新規作成・修正を行う
    :param request:
    :param competition_id:
    :rtype render|redirect:
    """
    if request.method == 'POST':
        # 編集時
        if competition_id:
            form = UpsertCompetitionForm(request.POST, instance=Competition.objects.get(pk=competition_id))
            if form.is_valid():
                form.save()
                return redirect('/competition/competition_list/')
            return render(request, 'cms/competition/upsert_competition.html', context={
                'competition_id': competition_id,
                'participate_teams': Participate.objects.filter(id=competition_id).all(),
                'form': form
            })
        # 新規作成
        form = UpsertCompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/competition/competition_list/')
        return render(request, 'cms/competition/upsert_competition.html', context={
            'form': form
        })
    return render(request, 'cms/competition/upsert_competition.html', context={
        'competition_id': competition_id,
        'participate_teams': Participate.objects.filter(id=competition_id).all(),
        'form': UpsertCompetitionForm(
            instance=Competition.objects.get(pk=competition_id)) if competition_id else UpsertCompetitionForm()
    })


def participate_competition(request, team_id):
    """
    大会に参加する
    :param request:
    :param int team_id:
    :rtype render:
    """
    if request.method == 'POST':
        form = ParticipateCompetitionForm(request.POST, initial={'team': Team.objects.get(pk=team_id)})
        if form.is_valid():
            form.instance.team = Team.objects.get(pk=team_id)
            form.save()
            return redirect('/competition/team/edit/{}/'.format(team_id))
        return render(request, 'cms/competition/participate_competition.html', context={
            'form': form
        })
    return render(request, 'cms/competition/participate_competition.html', context={
        'form': ParticipateCompetitionForm()
    })


def refusal_competition(request, team_id, competition_id):
    """
    大会参加を辞退する
    :param request:
    :param int team_id:
    :param int competition_id:
    :rtype redirect:
    """
    team = Team.objects.get(pk=team_id)
    competition = Competition.objects.get(pk=competition_id)
    if team and competition:
        participate = Participate.objects.filter(team=team, competition=competition)
        participate.delete()
    return redirect('competition/competition_list/edit/{}/'.format(competition_id))
