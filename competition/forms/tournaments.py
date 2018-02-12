from django import forms
from competition.infrastructure.tournament import MatchFormat, Participate, Tournament
from competition.infrastructure.discipline import Game


class UpsertTournamentForm(forms.ModelForm):
    error_css_class = 'has-error'
    Participate_TYPE_CHOICES = (
        ('team', 'チーム'),
        ('single', '個人')
    )
    ONLINE_CHOICES = (
        (True, 'オンライン'),
        (False, 'オフライン')
    )
    PUBLIC_CHOICES = (
        (True, 'パブリック'),
        (False, 'プライベート')
    )
    name = forms.CharField(required=True,
                           max_length=30,
                           label='大会名',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'}))
    game = forms.ModelChoiceField(required=True,
                                  queryset=Game.get_enabled_games(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'}),
                                  label='ゲーム')
    size = forms.IntegerField(required=True,
                              widget=forms.NumberInput(attrs={
                                  'class': 'form-control'}),
                              label='参加チーム数上限')
    participant_type = forms.ChoiceField(required=True,
                                         choices=Participate_TYPE_CHOICES,
                                         widget=forms.Select(attrs={
                                             'class': 'form-control'}),
                                         label='参加タイプ')
    full_name = forms.CharField(required=False,
                                max_length=80,
                                label='大会名(省略なし)',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control'}))
    organization = forms.CharField(required=False,
                                   max_length=255,
                                   label='運営団体',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control'}))
    website = forms.URLField(required=False,
                             label='大会公式サイトURL',
                             widget=forms.URLInput(attrs={
                                 'class': 'form-control'
                             }))
    date_start = forms.DateField(required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control datepicker'}),
                                 label='大会開始日')
    date_end = forms.DateField(required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control datepicker'}),
                               label='大会最終日')
    online = forms.ChoiceField(required=False,
                               choices=ONLINE_CHOICES,
                               widget=forms.Select(attrs={
                                   'class': 'form-control'}),
                               label='オンライン')
    public = forms.ChoiceField(required=False,
                               choices=PUBLIC_CHOICES,
                               widget=forms.Select(attrs={
                                   'class': 'form-control'}),
                               label='パブリック')
    location = forms.CharField(required=False,
                               max_length=255,
                               label='開催場所',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'}))
    description = forms.CharField(required=False,
                                  label='大会紹介文', max_length=1500,
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}))
    rules = forms.CharField(required=False,
                            label='ルール', max_length=10000,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control'}))
    prize = forms.CharField(required=False,
                            label='賞品', max_length=1500,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control'}))
    match_format = forms.ModelChoiceField(required=True,
                                          queryset=MatchFormat.get_enabled_match_format(),
                                          widget=forms.Select(attrs={
                                              'class': 'form-control'}),
                                          label='大会フォーマット')

    class Meta:
        model = Tournament
        fields = ('name', 'game', 'size', 'participant_type', 'full_name', 'organization', 'website',
                  'date_start', 'date_end', 'online', 'public', 'location', 'description', 'rules',
                  'prize', 'match_format')


class ParticipateTournamentForm(forms.ModelForm):
    tournament = forms.ModelChoiceField(queryset=Tournament.objects.filter(is_active=True),
                                        widget=forms.Select(attrs={
                                            'class': 'form-control'}),
                                        label='大会')

    class Meta:
        model = Participate
        fields = ('tournament',)
