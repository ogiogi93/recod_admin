from django import forms
from competition.models import Game, Team, Member


class UpsertTeamForm(forms.ModelForm):
    error_css_class = 'has-error'
    teamname = forms.CharField(max_length=50,
                               label='チーム名',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'}),
                               required=True,
                               error_messages={
                                   'required': 'そのチーム名は既に使用されています'
                               })
    description = forms.CharField(required=False, label='チーム紹介文',
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}),
                                  error_messages={
                                      'required': 'チーム紹介文を入力して下さい'})

    game = forms.ModelChoiceField(queryset=Game.objects.all(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'}),
                                  label='活動ゲーム')

    class Meta:
        model = Team
        fields = ('teamname', 'description', 'game')


class JoinTeam(forms.Form):
    team = forms.ChoiceField(label='チーム')

    def __init__(self, user_id, *args, **kwargs):
        super(JoinTeam, self).__init__(*args, **kwargs)
        self.fields['team'].candidate_teams = Member.get_candidate_teams(user_id)
