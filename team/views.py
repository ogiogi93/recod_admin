# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from account.models import CustomUser as User
from team.models import (
    Team,
    Member
)
from team.forms import EditTeamForm


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


def team_list(request):
    return render(request, 'cms/team/team_list.html', context={
        'teams': Team.get_all_teams_with_organizer()
    })
