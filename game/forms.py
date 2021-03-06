from django import forms
from service_api.models.disciplines import Discipline, Game, Map, Platform


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


class UpsertMapForm(forms.ModelForm):
    error_css_class = 'has-error'
    name = forms.CharField(max_length=50,
                           required=True,
                           label='マップ名',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'}))
    thumbnail_url = forms.URLField(required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control'}),
                                   label='マップ画像URL')

    class Meta:
        model = Map
        fields = ('name', 'thumbnail_url',)
