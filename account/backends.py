from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from account.models import CustomUser


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username, 'is_admin': True}
        else:
            kwargs = {'username': username, 'is_admin': True}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
