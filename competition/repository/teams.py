from django.shortcuts import render, redirect

from account.models import CustomUser as User
from competition.infrastructure.teams import Team, Member
from competition.infrastructure.tournament import Participate
from competition.forms.teams import UpsertTeamForm, JoinTeam


def upsert_team(request, user_id=None, team_id=None):
    """
    チームの新規作成・修正を行う
    :param request:
    :param int user_id:
    :param int team_id:
    :return:
    """
    if request.method == 'POST':
        # 編集時
        if team_id:
            form = UpsertTeamForm(request.POST, instance=Team.objects.get(pk=team_id))
            if form.is_valid():
                form.save()
                return redirect('/competition/team/')
            return render(request, 'cms/team/upsert_team.html', context={
                'user_id': user_id,
                'participate_tournaments': Participate.objects.filter(team_id=team_id).all(),
                'members': Member.objects.filter(team_id=team_id).order_by('id').all(),
                'form': form
            })
        # 新規追加
        form = UpsertTeamForm(request.POST)
        if form.is_valid():
            new_team = form.save()

            # Team Organizerとして登録しておく
            user = User.objects.get(pk=user_id)
            team = Team.objects.get(pk=new_team.pk)
            Member.objects.add_member(user, team, is_admin=True)
            return redirect('/competition/team/')
        return render(request, 'cms/team/upsert_team.html', context={
            'user_id': user_id,
            'form': form,
        })
    return render(request, 'cms/team/upsert_team.html', context={
        'user_id': user_id,
        'team_id': team_id,
        'participate_tournaments': Participate.objects.filter(team_id=team_id).all(),
        'members': Member.objects.filter(team_id=team_id).order_by('id').all(),
        'form': UpsertTeamForm(instance=Team.objects.get(pk=team_id)) if team_id else UpsertTeamForm()
    })


def delete_team(request, team_id):
    """
    チームを削除する
    :param request:
    :param int team_id:
    :rtype redirect:
    """
    team = Team.objects.get(pk=team_id)
    if team:
        team.delete()
    return redirect('/competition/team/')


def belong_teams(request, user_id):
    """
    指定されたユーザーの所属チームを返す
    :param request:
    :param int user_id:
    :rtype render:
    """
    return render(request, 'cms/user/edit_belong_team.html', context={
        'user_id': user_id,
        'nickname': User.objects.get(pk=user_id).username,
        'teams': Member.get_joined_teams(user_id),
        'team_form': JoinTeam(user_id)
    })


def join_team(request):
    """
    指定されたチームに所属させる
    :param request:
    :rtype redirect:
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)
        team = Team.objects.get(pk=request.POST.get('team_id'))
        if user and team:
            Member.objects.add_member(user, team, is_admin=False)
        return redirect('/competition/user_list/edit/{}/belong_team/'.format(user_id))
    return redirect('/competition/team/')


def secession_team(request, user_id, team_id):
    """
    チームから脱退する
    :param request:
    :param int user_id:
    :param int team_id:
    :rtype redirect:
    """

    user = User.objects.get(pk=user_id)
    team = Team.objects.get(pk=team_id)
    if user and team:
        member = Member.objects.filter(user=user).filter(team=team)
        member.delete()
        return redirect('/user_list/edit/{}/belong_team/'.format(user_id))
    return redirect('/user_list/edit/{}/belong_team/'.format(user_id))


def team_list(request):
    """
    チームリストを返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/team/team_list.html', context={
        'teams': Team.get_all_teams_with_organizer()
    })
