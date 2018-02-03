from django.shortcuts import render, redirect

from competition.models import Competition
from competition.forms.competitions import UpsertCompetitionForm


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
        'form': UpsertCompetitionForm(
            instance=Competition.objects.get(pk=competition_id)) if competition_id else UpsertCompetitionForm()
    })

