from django import forms
from competition.models import Competition, Game


class UpsertCompetitionForm(forms.ModelForm):
    error_css_class = 'has-error'
    name = forms.CharField(max_length=50,
                           label='大会名',
                           required=True,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'}),
                           error_messages={
                               'required': 'その大会名は既に使用されています'
                           })
    description = forms.CharField(required=False, label='大会紹介文',
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}),
                                  error_messages={
                                      'required': '大会紹介文を入力して下さい'})

    game = forms.ModelChoiceField(queryset=Game.objects.all(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'}),
                                  label='ゲーム')

    start_date = forms.DateField(required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control datepicker'}),
                                 label='大会開始日')
    end_date = forms.DateField(required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control datepicker'}),
                               label='大会最終日')

    class Meta:
        model = Competition
        fields = ('name', 'description', 'game', 'start_date', 'end_date', )
