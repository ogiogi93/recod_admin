from django import forms
from competition.models import Team, Member


class EditTeamForm(forms.ModelForm):
    error_css_class = 'has-error'
    is_active = forms.BooleanField(required=False, label='Active',
                                   widget=forms.CheckboxInput(attrs={
                                       'class': 'radio'}))
    teamname = forms.CharField(max_length=50,
                               label='チーム名',
                               required=True,
                               error_messages={
                                   'required': 'そのチーム名は既に使用されています'
                               })
    description = forms.CharField(required=False, label='チーム紹介文',
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}),
                                  error_messages={
                                      'required': 'チーム紹介文を入力して下さい'})

    class Meta:
        model = Team
        fields = ('is_active', 'teamname', 'description', )


class JoinTeam(forms.Form):
    team = forms.ChoiceField(label='チーム')

    def __init__(self, user_id, *args, **kwargs):
        super(JoinTeam, self).__init__(*args, **kwargs)
        self.fields['team'].candidate_teams = Member.get_candidate_teams(user_id)
