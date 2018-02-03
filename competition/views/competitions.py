from django.shortcuts import render, redirect

from competition.models import Competition
from competition.forms.competitions import CreateCompetitionForm


def create_competition(request):
    # 新規追加時はPOSTでくる
    if request.method == 'POST':
        form = CreateCompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/competition/competition_list/')
        return render(request, 'cms/competition/create_competition.html', context={
            'form': form
        })
    form = CreateCompetitionForm()
    return render(request, 'cms/competition/create_competition.html', context={
        'form': form
    })


def competition(request):
    return render(request, 'cms/competition/competition_list.html', context={
        'competitions': Competition.objects.order_by('date_created').all()
    })
