from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=BaseUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        u = self.create_user(email, password=password)
        u.is_admin = True
        u.save(using=self._db)
        return u


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name="username",
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    nickname = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    image = models.ImageField(upload_to='users/', default='defaults/default-profile-icon.jpg')

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def validate_unique(self, exclude=None):
        """Validate the field uniqueness"""
        CustomUser.objects.filter(email=self.email, is_active=False).delete()
        super(CustomUser, self).validate_unique(exclude)

    def display_name(self):
        if self.nickname:
            return self.nickname
        return self.username

    class Meta:
        db_table = 'account_customuser'
        managed = True


# Cross-database relationsの影響でフォーラムのmodel定義もこちらに配置しないと動かない
# https://stackoverflow.com/questions/26579231/unable-to-save-with-save-model-using-database-router
User = CustomUser


class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=False)
    title = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=1500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'forums'
        managed = False


class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=False)
    forum = models.ForeignKey(Forum, on_delete=False)
    title = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=1500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topics'
        managed = False


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=False)
    topic = models.ForeignKey(Topic, on_delete=False)
    description = models.CharField(max_length=1500, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'threads'
        managed = False
