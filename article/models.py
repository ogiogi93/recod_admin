from django.db import models
from django.utils import timezone

from account.models import CustomUser as User


class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField(max_length=255)
    original_image = models.URLField(max_length=255)
    url = models.URLField(max_length=255, default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    image_width = models.FloatField(null=True, default=0)
    image_height = models.FloatField(null=True, default=0)

    class Meta:
        managed = False
        db_table = 'articles'
