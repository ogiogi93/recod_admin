from django.db import models
from django.utils import timezone

from service_api.models.users import CustomUser as User
from service_api.models.disciplines import Game


class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=False)
    game = models.ForeignKey(Game, on_delete=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail_url = models.URLField()
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

    def __str__(self):
        return self.title
