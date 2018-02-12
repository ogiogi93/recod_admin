from django.shortcuts import render, redirect

from competition.api.tournaments import (
    delete_api_tournament,
    get_tournament_matches,
    refusal_api_participate,
    upsert_api_tournament,
    upsert_api_participate,
)
from competition.infrastructure.tournament import Game, Match, MatchTeam, Tournament, Participate
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
                return redirect('/competition/tournament/')
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
            return redirect('/competition/tournament/')
        return render(request, 'cms/tournament/upsert_tournament.html', context={
            'form': form
        })
    return render(request, 'cms/tournament/upsert_tournament.html', context={
        'tournament_id': tournament_id,
        'tournament_api_id': Tournament.objects.get(pk=tournament_id).api_tournament_id if tournament_id else None,
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
        form.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).exclude(
            participate__team__id=team_id)
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
    form.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).exclude(
        participate__team__id=team_id)
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
    return redirect('/competition/tournament/edit/{}/'.format(tournament_id))


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
    return redirect('/competition/tournament')


def get_and_upsert_matches(request, tournament_id):
    """
    Toonament APIからマッチ情報を取得し, DBに新規登録or更新をする
    :param request:
    :param tournament_id:
    :rtype redirect:
    """
    tournament = Tournament.objects.get(pk=tournament_id)
    entities = get_tournament_matches(api_tournament_id=tournament.api_tournament_id)
    for entity in entities:
        # マッチ情報を登録・更新
        match = Match.objects.update_or_create(
            api_match_id=entity.id(),
            game=Game.objects.get(pk=tournament.game.id),
            tournament=tournament,
            defaults={
                'stage_number': entity.stage_number(),
                'group_number': entity.group_number(),
                'round_number': entity.round_number(),
                'match_format': tournament.match_format,
                'status': entity.status(),
            })
        for opponent in entity.opponents():
            # マッチ詳細情報を登録・更新
            participate_id = opponent.participant().id()
            if not participate_id:
                # 全戦分のマッチ情報が帰ってくるので勝ち上がりチームがまだ分からない(participate_id=None)時は処理を抜ける
                continue
            MatchTeam.objects.update_or_create(
                match=match[0],
                team=Participate.objects.get(api_participate_id=participate_id).team,
                defaults={
                    'result': opponent.result(),
                    'score': opponent.score()
                })
    return redirect('/competition/tournament/edit/{}/'.format(tournament_id))
