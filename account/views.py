from django.shortcuts import render, redirect, get_object_or_404

from account.models import CustomUser as User
from account.forms import (
    RegisterForm,
    EditUserProfile
)
from competition.models import Member


def user_list(request):
    """
    ユーザーリストを返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/user/user_list.html', context={
        'users': User.objects.all()
    })


def upsert_user(request, user_id=None):
    """
    ユーザーを新規追加 or 修正する
    :param request:
    :param int user_id:
    :rtype render|redirect:
    """
    if request.method == 'POST':
        # 編集時はuser_idが設定されている
        if user_id:
            form = EditUserProfile(request.POST, instance=User.objects.get(pk=user_id))
            if form.is_valid():
                form.save()
                return redirect('/user/user_list/')
            return render(request, 'cms/user/upsert_user.html', context={
                'form': form,
                'user_id': user_id
            })
        #  user_idが指定されてされていなければ新規登録
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/user_list/')
        return render(request, 'cms/user/upsert_user.html', context={
            'form': form,
        })
    return render(request, 'cms/user/upsert_user.html', context={
        'form': EditUserProfile(instance=User.objects.get(pk=user_id)) if user_id else RegisterForm(),
        'joined_teams': Member.objects.filter(user_id=user_id),
        'user_id': user_id
    })


def delete_user(request, user_id):
    """
    ユーザーを削除する
    :param request:
    :param int user_id:
    :rtype redirect:
    :param request:
    """
    user = get_object_or_404(User, pk=user_id)
    if user:
        user.delete()
    return redirect('/user/user_list/')
