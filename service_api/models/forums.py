from django.db import models

from service_api.models.users import CustomUser as User


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
