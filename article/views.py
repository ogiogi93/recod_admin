from django.shortcuts import render, redirect

from article.forms import UpsertArticleForm
from service_api.models.articles import Article
from service_api.models.users import CustomUser as User


def article_list(request):
    """
    記事リストを返す
    :param request:
    :rtype render:
    """
    return render(request, 'cms/article/article_list.html', context={
        'articles': Article.objects.select_related('user').order_by('-created_at').all()
    })


def upsert_article(request, article_id=None):
    """
    記事を新規投稿または編集をする
    :param request:
    :param int article_id:
    :return:
    """
    if request.method == 'POST':
        # 編集時
        if article_id:
            form = UpsertArticleForm(request.POST, instance=Article.objects.get(pk=article_id))
            # TODO: ログイン機能追加したらログインユーザのuser_idを設定する
            if form.is_valid():
                form.save()
                return redirect('/article/')
            return render(request, 'cms/article/upsert_article.html', context={
                'form': form,
                'article_id': article_id
            })
        # 新規投稿
        form = UpsertArticleForm(request.POST)
        form.instance.user = User.objects.get(pk=1)
        if form.is_valid():
            form.save()
            return redirect('/article/')
        return render(request, 'cms/article/upsert_article.html', context={
            'form': form,
            'article_id': article_id
        })
    return render(request, 'cms/article/upsert_article.html', context={
        'form': UpsertArticleForm(instance=Article.objects.get(pk=article_id)) if article_id else UpsertArticleForm(),
        'article_id': article_id
    })


def delete_article(request, article_id):
    """
    指定の記事を削除する
    :param request:
    :param int article_id:
    :rtype redirect:
    """
    article = Article.objects.get(pk=article_id)
    if article:
        article.delete()
    return redirect('/article/')
