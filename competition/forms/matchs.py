from django import forms
from competition.infrastructure.tournament import MatchTeam


class UpdateMatchForm(forms.ModelForm):
    error_css_class = 'has-error'
    STATUS_CHOICES = {
        (1, '勝利'),
        (2, '引き分け'),
        (3, '敗北')
    }
    id = forms.IntegerField(widget=forms.HiddenInput())
    result = forms.ChoiceField(required=True,
                               choices=STATUS_CHOICES,
                               widget=forms.Select(attrs={
                                   'class': 'form-control'}),
                               label='結果')
    score = forms.IntegerField(required=True,
                               widget=forms.NumberInput(attrs={
                                   'class': 'form-control'}),
                               label='スコア'
                               )

    class Meta:
        model = MatchTeam
        fields = ('id', 'result', 'score')
