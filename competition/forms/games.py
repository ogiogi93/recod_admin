from django import forms
from competition.infrastructure.discipline import Discipline, Game, Platform


class UpsertGameForm(forms.ModelForm):
    error_css_class = 'has-error'
    platform = forms.ModelChoiceField(required=True,
                                      queryset=Platform.objects.all(),
                                      widget=forms.Select(attrs={
                                          'class': 'form-control'}),
                                      label='プラットフォーム')
    discipline = forms.ModelChoiceField(required=True,
                                        queryset=Discipline.objects.filter(is_active=True).all(),
                                        widget=forms.Select(attrs={
                                            'class': 'form-control'}),
                                        label='ゲームタイトル')
    home_url = forms.URLField(required=False,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control'}),
                              label='公式サイト')
    date_released = forms.DateField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control datepicker'}),
                                    label='発売日')

    class Meta:
        model = Game
        fields = ('platform', 'discipline', 'home_url', 'date_released')
