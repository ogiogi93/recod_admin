from django.shortcuts import render, redirect
from django.http import JsonResponse

from competition.api.tournaments import update_match_result
from competition.forms.matchs import UpdateMatchForm
from competition.infrastructure.tournament import Match, MatchTeam, Team


def update_match(request, match_id):
    """
    指定されたマッチの結果をチームごとに更新する
    :param request:
    :param int match_id:
    :param int|None match_team_id:
    :return JsonResponse:
    """
    if request.method == 'POST':
        team_match_id = request.POST.get('form-id')
        opponent_team_match_id = request.POST.get('form_opponent-id')
        form = UpdateMatchForm(request.POST, prefix='form', instance=MatchTeam.objects.get(pk=team_match_id))
        form_opponent = UpdateMatchForm(
            request.POST, prefix='form_opponent', instance=MatchTeam.objects.get(pk=opponent_team_match_id))
        for f in [form, form_opponent]:
            if f.is_valid():
                match_team_id = f.instance.id
                match_team = MatchTeam.objects.select_related('match', 'match__tournament', 'team').get(
                    pk=match_team_id)
                # Toornament APIに登録する
                updated = update_match_result(api_tournament_id=match_team.match.tournament.api_tournament_id,
                                              api_match_id=match_team.match.api_match_id,
                                              api_opponent_id=match_team.api_opponent_id,
                                              status='completed',
                                              result=f.instance.result,
                                              score=f.instance.score)
                if not updated:
                    continue
                f.save()
            else:
                return _render_match(request, match_id)
        # Match.statusも更新しておく
        match = Match.objects.get(id=match_id)
        match.status = 'completed'
        match.save()
        return redirect('/competition/tournament/edit/{}/'.format(match.tournament_id))
    return _render_match(request, match_id)


def _render_match(request, match_id, form=None, form_opponent=None,
                  match_team_id=None, opponent_match_team_id=None, team_name=None, opponent_team_name=None):
    """
    マッチ更新ページをformと共に返す
    :param request:
    :param match_id:
    :return:
    """
    # 対戦チームそれぞれのformを生成する
    match_teams = MatchTeam.objects.select_related('team').filter(match_id=match_id)
    for mt in match_teams:
        if not match_team_id:
            match_team_id = mt.id
            form = UpdateMatchForm(instance=mt, prefix='form')
            form.instance.id = match_team_id
            team_name = mt.team.name
        else:
            opponent_match_team_id = mt.id
            form_opponent = UpdateMatchForm(instance=mt, prefix='form_opponent')
            form_opponent.instance.id = opponent_match_team_id
            opponent_team_name = mt.team.name
    return render(request, 'cms/tournament/match/update_match.html', context={
        'match_id': match_id,
        'form': form,
        'opponent_form': form_opponent,
        'match_team_id': match_team_id,
        'opponent_match_team_id': opponent_match_team_id,
        'team_name': team_name,
        'opponent_team_name': opponent_team_name
    })
