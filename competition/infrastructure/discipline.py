from django.db import models


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'platforms'
        managed = False

    def __str__(self):
        return self.name


class Discipline(models.Model):
    id = models.AutoField(primary_key=True)
    api_discipline_id = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    short_name = models.CharField(max_length=30)
    copy_right = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'discipline'
        managed = False

    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.ForeignKey(Platform, on_delete=False)
    discipline = models.ForeignKey(Discipline, on_delete=False)
    logo_url = models.URLField()
    home_url = models.URLField()
    is_active = models.BooleanField(default=True)
    date_released = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'games'
        managed = False
        unique_together = ('discipline', 'platform', )

    def __str__(self):
        return '{} ({})'.format(self.discipline.name, self.platform.name)
