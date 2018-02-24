from django.db import models
from django.utils import timezone


class VideoAuthor(models.Model):
    id = models.BigAutoField(primary_key=True)
    platform = models.ForeignKey('VideoPlatform', on_delete=False)
    platform_author_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    home_url = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=255, blank=True, null=True)
    view_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    subscriber_count = models.BigIntegerField()
    video_count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'video_authors'
        unique_together = (('platform_author_id', 'platform'),)


class VideoPlatform(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'video_platforms'


class VideoTag(models.Model):
    video = models.OneToOneField('Video', related_name='tag', primary_key=True)
    tags = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'video_tags'


class Video(models.Model):
    id = models.BigAutoField(primary_key=True)
    article = models.ForeignKey('Article', on_delete=False)
    platform = models.ForeignKey('VideoPlatform', on_delete=False)
    platform_video_id = models.CharField(max_length=255)
    video_author = models.ForeignKey('VideoAuthor', on_delete=False)
    thumbnail_url = models.CharField(max_length=255)
    thumbnail_width = models.IntegerField(default=None)
    thumbnail_height = models.IntegerField(default=None)
    duration = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    view_count = models.BigIntegerField(blank=True, null=True)
    like_count = models.BigIntegerField(blank=True, null=True)
    dislike_count = models.BigIntegerField(blank=True, null=True)
    comment_count = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'videos'
        unique_together = (('platform_video_id', 'platform'),)
