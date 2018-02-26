from django import forms
from account.models import Forum, Topic, Thread


class UpsertForumForm(forms.ModelForm):
    error_css_class = 'has-error'
    title = forms.CharField(required=True,
                            max_length=30,
                            label='タイトル',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'}))

    description = forms.CharField(required=False,
                                  label='本文', max_length=10000,
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}))

    class Meta:
        model = Forum
        fields = ('title', 'description', )


class UpsertTopicForm(forms.ModelForm):
    error_css_class = 'has-error'
    title = forms.CharField(required=True,
                            max_length=30,
                            label='タイトル',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'}))

    description = forms.CharField(required=False,
                                  label='本文', max_length=10000,
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}))

    class Meta:
        model = Topic
        fields = ('title', 'description', )


class UpsertThreadForm(forms.ModelForm):
    error_css_class = 'has-error'
    description = forms.CharField(required=False,
                                  label='本文', max_length=10000,
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}))

    class Meta:
        model = Thread
        fields = ('description', )
