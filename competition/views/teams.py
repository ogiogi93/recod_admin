from django.shortcuts import render, redirect

from account.models import CustomUser as User
from competition.models import Team, Member
from competition.forms.teams import EditTeamForm, JoinTeam


def create_team_page(request, user_id=None):
    if not user_id:
        return redirect('/team_list/')
    # 新規追加時はPOSTでくる
    if request.method == 'POST':
        form = EditTeamForm(request.POST)
        if form.is_valid():
            new_team = form.save()

            # Team Organizerとして登録しておく
            user = User.objects.get(pk=user_id)
            team = Team.objects.get(pk=new_team.pk)
            Member.objects.add_member(user, team, is_admin=True)
            return redirect('/team_list/')
        return render(request, 'cms/team/create_team.html', context={
            'user_id': user_id,
            'form': form
        })
    form = EditTeamForm()
    return render(request, 'cms/team/create_team.html', context={
        'user_id': user_id,
        'form': form
    })


def edit_team(request, team_id=None):
    if not team_id:
        return redirect('/team_list/')
    team = Team.objects.get(pk=team_id)
    # 編集時はPOSTでくる
    if request.method == 'POST':
        form = EditTeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('/team_list/')
        return render(request, 'cms/team/edit_team.html', context={
            'team_id': team_id,
            'form': form
        })
    return render(request, 'cms/team/edit_team.html', context={
        'team_id': team_id,
        'form': EditTeamForm(instance=team)
    })


def delete_team(request, team_id=None):
    team = Team.objects.get(pk=team_id)
    if team:
        team.delete()
    return redirect('/team_list/')


def joined_teams(request, user_id=None):
    if not user_id:
        return redirect('/team_list/')
    return render(request, 'cms/user/edit_join_team.html', context={
        'user_id': user_id,
        'nickname': list(User.objects.values_list('nickname', flat=True).filter(id=user_id))[0],
        'teams': Member.get_joined_teams(user_id),
        'team_form': JoinTeam(user_id)
    })


def join_team(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)
        team = Team.objects.get(pk=request.POST.get('team_id'))
        if user and team:
            Member.objects.add_member(user, team, is_admin=False)
        return redirect('/user_list/edit/{}/joined_team/'.format(user_id))
    return redirect('/team_list/')


def secession_team(request, user_id, team_id):
    user = User.objects.get(pk=user_id)
    team = Team.objects.get(pk=team_id)
    if user and team:
        member = Member.objects.filter(user=user).filter(team=team)
        member.delete()
        return redirect('/user_list/edit/{}/joined_team/'.format(user_id))
    return redirect('/user_list/edit/{}/joined_team/'.format(user_id))


def team_list(request):
    return render(request, 'cms/team/team_list.html', context={
        'teams': Team.get_all_teams_with_organizer()
    })
