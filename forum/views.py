from django.shortcuts import render, redirect

from account.models import CustomUser as User
from account.models import Forum, Thread, Topic
from forum.forms import UpsertForumForm, UpsertThreadForm, UpsertTopicForm


def upsert_forum(request, forum_id=None):
    """
    フォーラムの新規作成・修正を行う
    :param request:
    :param int forum_id:
    :rtype render|redirect:
    """
    if request.method == 'POST':
        # 編集時
        if forum_id:
            form = UpsertForumForm(request.POST, instance=Forum.objects.get(pk=forum_id))
            if form.is_valid():
                form.save()
                return redirect('/forum/')
            return render(request, 'cms/forum/upsert_forum.html', context={
                'form': form,
                'forum_id': forum_id
            })
        # 新規追加
        form = UpsertForumForm(request.POST)
        # TODO: ログインユーザのIDを入れる
        form.instance.user = User.objects.get(pk=1)
        if form.is_valid():
            form.save()
            return redirect('/forum/')
        return render(request, 'cms/forum/upsert_forum.html', context={
            'form': form
        })
    return render(request, 'cms/forum/upsert_forum.html', context={
        'form': UpsertForumForm(instance=Forum.objects.get(pk=forum_id)) if forum_id else UpsertForumForm(),
        'forum_id': forum_id
    })


def delete_forum(request, forum_id):
    """
    フォーラムを削除する
    :param request:
    :param int forum_id:
    :rtype redirect:
    """
    forum = Forum.objects.get(pk=forum_id)
    if forum:
        forum.delete()
    return redirect('/forum/')


def forum_list(request):
    """
    フォーラムのリストを返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/forum/forum_list.html', context={
        'forums': Forum.objects.select_related('user').filter(is_active=True)
    })


def upsert_topic(request, forum_id, topic_id=None):
    """
    トピックの新規作成・修正を行う
    :param request:
    :param int forum_id:
    :param int topic_id:
    :rtype render|redirect:
    """
    if request.method == 'POST':
        # 編集時
        if topic_id:
            form = UpsertTopicForm(request.POST, instance=Topic.objects.get(pk=topic_id))
            if form.is_valid():
                form.save()
                return redirect('/forum/{}/'.format(forum_id))
            return render(request, 'cms/forum/upsert_topic.html', context={
                'form': form,
                'forum_id': forum_id,
                'topic_id': topic_id
            })
        # 新規追加
        form = UpsertTopicForm(request.POST)
        form.instance.forum = Forum.objects.get(pk=forum_id)
        # TODO: ログインユーザのIDを入れる
        form.instance.user = User.objects.get(pk=1)
        if form.is_valid():
            form.save()
            return redirect('/forum/{}/'.format(forum_id))
        return render(request, 'cms/forum/upsert_topic.html', context={
            'form': form,
            'forum_id': forum_id,
        })
    return render(request, 'cms/forum/upsert_topic.html', context={
        'form': UpsertTopicForm(instance=Topic.objects.get(pk=topic_id)) if topic_id else UpsertTopicForm(),
        'forum_id': forum_id,
        'topic_id': topic_id
    })


def delete_topic(request, forum_id, topic_id):
    """
    トピックを削除する
    :param request:
    :param int forum_id:
    :param int topic_id:
    :rtype redirect:
    """
    topic = Topic.objects.get(pk=topic_id)
    if topic:
        topic.delete()
    return redirect('/forum/{}/'.format(forum_id))


def topic_list(request, forum_id):
    """
    フォーラムのリストを返す
    :param request:
    :param int forum_id:
    :rtype render:
    """
    return render(request, 'cms/forum/topic_list.html', context={
        'forum_id': forum_id,
        'topics': Topic.objects.select_related('user').filter(is_active=True, forum_id=forum_id)
    })


def upsert_thread(request, forum_id, topic_id, thread_id=None):
    """
    スレッドの新規作成・修正を行う
    :param request:
    :param int forum_id:
    :param int topic_id:
    :param int thread_id:
    :rtype render|redirect:
    """
    if request.method == 'POST':
        # 編集時
        if thread_id:
            form = UpsertThreadForm(request.POST, instance=Thread.objects.get(pk=thread_id))
            if form.is_valid():
                form.save()
                return redirect('/forum/{}/{}/'.format(forum_id, topic_id))
            return render(request, 'cms/forum/upsert_thread.html', context={
                'form': form,
                'forum_id': forum_id,
                'topic_id': topic_id,
                'thread_id': thread_id
            })
        # 新規追加
        form = UpsertThreadForm(request.POST)
        form.instance.forum = Forum.objects.get(pk=forum_id)
        form.instance.topic = Topic.objects.get(pk=topic_id)
        # TODO: ログインユーザのIDを入れる
        form.instance.user = User.objects.get(pk=1)
        if form.is_valid():
            form.save()
            return redirect('/forum/{}/{}/'.format(forum_id, topic_id))
        return render(request, 'cms/forum/upsert_thread.html', context={
            'form': form,
            'forum_id': forum_id,
            'topic_id': topic_id,
            'thread_id': thread_id
        })
    return render(request, 'cms/forum/upsert_thread.html', context={
        'form': UpsertThreadForm(instance=Thread.objects.get(pk=thread_id)) if thread_id else UpsertThreadForm(),
        'forum_id': forum_id,
        'topic_id': topic_id,
        'thread_id': thread_id
    })


def delete_thread(request, forum_id, topic_id, thread_id):
    """
    トピックを削除する
    :param request:
    :param int forum_id:
    :param int topic_id:
    :param int thread_id:
    :rtype redirect:
    """
    thread = Thread.objects.get(pk=thread_id)
    if thread:
        thread.delete()
    return redirect('/forum/{}/{}/'.format(forum_id, topic_id))


def thread_list(request, forum_id, topic_id):
    """
    フォーラムのリストを返す
    :param request:
    :param int forum_id:
    :param int topic_id:
    :rtype render:
    """
    return render(request, 'cms/forum/thread_list.html', context={
        'forum_id': forum_id,
        'topic_id': topic_id,
        'threads': Thread.objects.select_related('user').filter(is_active=True, topic_id=topic_id)
    })
