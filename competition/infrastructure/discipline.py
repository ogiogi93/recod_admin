from django.db import models


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    display_name = models.CharField(max_length=255, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'platforms'
        managed = False

    def __str__(self):
        return self.display_name


class Discipline(models.Model):
    id = models.AutoField(primary_key=True)
    api_discipline_id = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=30)
    copy_rights = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'disciplines'
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
        return '{} ({})'.format(self.discipline.name, self.platform.display_name)

    @classmethod
    def get_enabled_games(cls):
        return cls.objects.filter(discipline__is_active=True).select_related('discipline', 'platform').all()


class Map(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=False)
    name = models.CharField(max_length=255, null=False)
    logo_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maps'
        managed = False
        unique_together = ('game', 'name', )
