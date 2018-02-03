from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from account.models import CustomUser as User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50,
                               label='ユーザーID',
                               required=True,
                               error_messages={
                                   'required': 'そのユーザ名は既に使用されています'
                               })
    email = forms.EmailField(label='メールアドレス',
                             required=True,
                             error_messages={
                                 'required': 'そのメールアドレスは既に使用されています'
                             })

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].help_text = None
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワードの確認'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].help_text = None


class EmailChangeForm(forms.Form):
    error_messages = {
        'email_mismatch': "The two e-mail address fields do not match.",
        'email_inuse': "This e-mail address cannot be used. Please select a different e-mail address.",
        'password_incorrect': "Incorrect password.",
    }

    current_password = forms.CharField(
        label="現在のパスワード",
        widget=forms.PasswordInput,
        required=True
    )

    new_email1 = forms.EmailField(
        label="新しいメールアドレス",
        max_length=254,
        required=True
    )

    new_email2 = forms.EmailField(
        label="新しいメールアドレス（確認用）",
        max_length=254,
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        """
        Validates that the password field is correct.
        """
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect', )
        return current_password

    def clean_new_email1(self):
        """
        Prevents an e-mail address that is already registered from being registered by a different user.
        """
        email1 = self.cleaned_data.get('new_email1')
        if User.objects.filter(email=email1).count() > 0:
            raise forms.ValidationError(self.error_messages['email_inuse'], code='email_inuse', )
        return email1

    def clean_new_email2(self):
        """
        Validates that the confirm e-mail address's match.
        """
        email1 = self.cleaned_data.get('new_email1')
        email2 = self.cleaned_data.get('new_email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError(self.error_messages['email_mismatch'], code='email_mismatch', )
        return email2

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email1']
        if commit:
            self.user.save()
        return self.user


class EditUserProfile(forms.ModelForm):
    error_css_class = 'has-error'
    is_admin = forms.BooleanField(required=False, label='Adminユーザー',
                                  widget=forms.CheckboxInput(attrs={
                                      'class': 'radio'}))
    username = forms.CharField(required=True, label='ユーザーネーム',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'}),
                               error_messages={
                                   'required': '新しいユーザーネームを入力して下さい'})
    nickname = forms.CharField(required=True, label='ニックネーム',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control'}),
                               error_messages={
                                   'required': '新しいニックネームを入力して下さい'})
    email = forms.EmailField(required=True, max_length=254, label='メールアドレス',
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control'}),
                             error_messages={
                                 'required': '正しいメールアドレスを入力して下さい'})
    description = forms.CharField(required=False, label='自己紹介文',
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control'}),
                                  error_messages={
                                      'required': '自己紹介文を入力して下さい'})

    class Meta:
        model = User
        fields = ('is_admin', 'username', 'nickname', 'email', 'description')


class EditProfilePassword(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect': "入力されたパスワードは間違っています"}
    old_password = forms.CharField(required=True, label='現在のパスワード',
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control'}),
                                   error_messages={
                                       'required': '現在のパスワードを入力してください'})

    new_password1 = forms.CharField(required=True, label='新しいパスワード',
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control'}),
                                    error_messages={
                                        'required': '新しいパスワードを入力してください'})
    new_password2 = forms.CharField(required=True, label='新しいパスワード(確認用)',
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control'}),
                                    error_messages={
                                        'required': '新しいパスワードを入力してください'})
