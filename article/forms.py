from django import forms

from competition.infrastructure.article import Article
from competition.infrastructure.discipline import Game


class UpsertArticleForm(forms.ModelForm):
    error_css_class = 'has-error'
    title = forms.CharField(required=True,
                            max_length=30,
                            label='タイトル',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'}))

    content = forms.CharField(required=False,
                              label='本文', max_length=10000,
                              widget=forms.Textarea(attrs={
                                  'class': 'form-control'}))
    thumbnail_url = forms.URLField(required=False,
                                   label='サムネイル画像URL',
                                   widget=forms.URLInput(attrs={
                                       'class': 'form-control'
                                   }))
    game = forms.ModelChoiceField(queryset=Game.get_enabled_games(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'}),
                                  label='対象ゲーム')

    class Meta:
        model = Article
        fields = ('title', 'content', 'thumbnail_url', 'game')
