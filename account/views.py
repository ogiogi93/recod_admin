from django.shortcuts import render, redirect, get_object_or_404

from account.models import CustomUser as User
from account.forms import EditUserProfile


def add_user(request):
    # 新規追加時はPOSTでくる
    if request.method == 'POST':
        form = EditUserProfile(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_list/')
        return render(request, 'cms/user/add_user.html', context={
            'form': form
        })
    form = EditUserProfile()
    return render(request, 'cms/user/add_user.html', context={
        'form': form
    })


def edit_user(request, user_id=None):
    # なぜかuser_idがなかった時はListページに飛ばす
    if not user_id:
        return redirect('/user_list/')

    user = User.objects.get(pk=user_id) # 修正時にPOSTでくる
    if request.method == 'POST':
        form = EditUserProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/user_list/')
        else:
            return render(request, 'cms/user/edit_user.html', context={
                'user_id': user_id,
                'form': form
            })
    return render(request, 'cms/user/edit_user.html', context={
        'user_id': user_id,
        'form': EditUserProfile(instance=User.objects.get(pk=user_id))
    })


def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user:
        user.delete()
    return redirect('/user_list/')


def user_list(request):
    return render(request, 'cms/user/user_list.html', context={
        'users': User.objects.all()
    })
