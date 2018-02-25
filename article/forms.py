from django import forms
from article.models import Article


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
    image = forms.URLField(required=False,
                           label='サムネイル画像URL',
                           widget=forms.URLInput(attrs={
                               'class': 'form-control'
                           }))

    class Meta:
        model = Article
        fields = ('title', 'content', 'image', )
