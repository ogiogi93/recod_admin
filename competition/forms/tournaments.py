from django import forms
from competition.infrastructure.tournament import MatchFormat, Participate, Tournament
from competition.infrastructure.discipline import Discipline


class UpsertTournamentForm(forms.ModelForm):
    error_css_class = 'has-error'
    name = forms.CharField(max_length=30,
                           label='大会名',
                           required=True,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'}))
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(),
                                        widget=forms.Select(attrs={
                                            'class': 'form-control'}),
                                        label='ゲーム')
    size = forms.IntegerField(required=True,
                              widget=forms.NumberInput(attrs={
                                  'class': 'form-control'}),
                              label='参加チーム数上限')
    participant_type = forms.ModelChoiceField(queryset=Tournament.ParticipantType.choices(),
                                              required=True,
                                              widget=forms.Select(attrs={
                                                  'class': 'form-control'}),
                                              label='参加タイプ')
    full_name = forms.CharField(max_length=80,
                                label='大会名(省略なし)',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control'}))
    organization = forms.CharField(max_length=255,
                                   label='運営団体',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control'}))
    website = forms.URLField(label='大会公式サイトURL',
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
    online = forms.BooleanField(widget=forms.NullBooleanSelect(attrs={
        'class': 'form-control'}), label='オンライン')
    public = forms.BooleanField(widget=forms.NullBooleanSelect(attrs={
        'class': 'form-control'}), label='パブリック')
    location = forms.CharField(max_length=255,
                               label='開催場所',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'}))
    description = forms.CharField(label='大会紹介文', max_length=1500,
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}))
    rules = forms.CharField(label='ルール', max_length=10000,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control'}))
    prize = forms.CharField(label='賞品', max_length=1500,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control'}))
    match_format = forms.ModelChoiceField(queryset=MatchFormat.objects.all(),
                                          required=True,
                                          widget=forms.Select(attrs={
                                              'class': 'form-control'}),
                                          label='大会フォーマット')

    class Meta:
        model = Tournament
        fields = ('name', 'discipline', 'size', 'participant_type', 'full_name', 'organization', 'website',
                  'date_start', 'date_end', 'online', 'public', 'location', 'country', 'description', 'rules',
                  'prize', 'match_format')


class ParticipateTournamentForm(forms.ModelForm):
    tournament = forms.ModelChoiceField(queryset=Tournament.objects.filter(is_active=True).all(),
                                        widget=forms.Select(attrs={
                                            'class': 'form-control'}),
                                        label='大会')

    class Meta:
        model = Participate
        fields = ('tournament',)
