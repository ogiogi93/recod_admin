from django import forms
from competition.models import Competition, Schedule


class CreateCompetitionForm(forms.ModelForm):
    error_css_class = 'has-error'
    name = forms.CharField(max_length=50,
                           label='大会名',
                           required=True,
                           error_messages={
                               'required': 'その大会名は既に使用されています'
                           })
    description = forms.CharField(required=False, label='大会紹介文',
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}),
                                  error_messages={
                                      'required': '大会紹介文を入力して下さい'})

    class Meta:
        model = Competition
        fields = ('name', 'description',)


class CreateSchedule(forms.Form):
    error_css_class = 'has-error'
    name = forms.CharField(max_length=50,
                           label='マッチ名',
                           required=True)
    start_datetime = forms.DateTimeField(label='マッチ開始時間',
                                         required=True)
    competition = forms.ChoiceField(label='大会')

    class Meta:
        model = Schedule
        fields = ('name', 'start_datetime', 'competition', )

    def __init__(self, *args, **kwargs):
        super(CreateSchedule, self).__init__(*args, **kwargs)
        self.fields['competition'].choices = Competition.get_competitions()
