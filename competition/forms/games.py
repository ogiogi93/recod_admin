from django import forms
from competition.models import Game, Platform


class UpsertGameForm(forms.ModelForm):
    error_css_class = 'has-error'
    title = forms.CharField(max_length=50,
                            label='ゲームタイトル',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'}),
                            required=True,
                            )
    home_url = forms.URLField(required=True,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control'}),
                              label='公式サイト')
    date_released = forms.DateField(required=True,
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control datepicker'}),
                                    label='発売日')
    platform = forms.ModelChoiceField(queryset=Platform.objects.all(),
                                      widget=forms.Select(attrs={
                                          'class': 'form-control'}),
                                      label='プラットフォーム')

    class Meta:
        model = Game
        fields = ('title', 'home_url', 'date_released', 'platform')
