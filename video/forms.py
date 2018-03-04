from django import forms

from service_api.models.articles import Article
from service_api.models.disciplines import Game
from service_api.models.videos import Video, VideoAttribute


class UpsertVideoForm(forms.Form):
    platform_video_id = forms.CharField(required=True,
                                        widget=forms.TextInput(attrs={
                                            'class': 'form-control'}),
                                        label='Youtubeの動画ID')

    game = forms.ModelChoiceField(required=True,
                                  queryset=Game.objects.filter(is_active=True).all(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'}),
                                  label='ゲームタイトル')
    article = forms.ModelChoiceField(required=False,
                                     queryset=Article.objects.filter(is_active=True).all(),
                                     widget=forms.Select(attrs={
                                         'class': 'form-control'}),
                                     label='記事タイトル')


class UpsertVideoAttributeForm(forms.ModelForm):
    video = forms.ModelChoiceField(required=True,
                                   queryset=Video.objects.filter(enabled=True).all(),
                                   widget=forms.Select(attrs={
                                       'class': 'form-control'}),
                                   label='動画タイトル')
    game = forms.ModelChoiceField(required=True,
                                  queryset=Game.objects.filter(is_active=True).all(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'}),
                                  label='ゲームタイトル')
    article = forms.ModelChoiceField(required=False,
                                     queryset=Article.objects.filter(is_active=True).all(),
                                     widget=forms.Select(attrs={
                                         'class': 'form-control'}),
                                     label='記事タイトル')

    class Meta:
        model = VideoAttribute
        fields = ('video', 'game', 'article', )
