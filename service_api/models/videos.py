from django.db import models


class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    platform_id = models.IntegerField(null=False)
    platform_author_id = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    home_url = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=1024)
    enabled = models.BooleanField(null=False)
    view_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    subscriber_count = models.BigIntegerField()
    video_count = models.IntegerField()
    modified_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'video_authors'
        managed = False


class Platform(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(null=False)

    class Meta:
        db_table = 'video_platforms'
        managed = False


class Video(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey('Author', on_delete=False)
    platform = models.ForeignKey('Platform', on_delete=False)
    platform_video_id = models.CharField(max_length=255, null=False)
    platform_category_id = models.IntegerField()
    title = models.TextField(null=False)
    original_title = models.TextField(null=False)
    thumbnail_url = models.CharField(max_length=1024)
    enabled = models.BooleanField(null=False)
    original_url = models.CharField(max_length=1024)
    mp4_url = models.CharField(max_length=1024)
    duration = models.IntegerField()
    width = models.IntegerField(default=640)
    height = models.IntegerField(default=360)
    view_count = models.BigIntegerField()
    like_count = models.BigIntegerField()
    dislike_count = models.BigIntegerField()
    favorite_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    modified_at = models.DateTimeField(null=False)
    published_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'videos'
        managed = False


class VideoText(models.Model):
    video = models.OneToOneField('Video', related_name='text', primary_key=True, on_delete=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video_texts'
        managed = False
