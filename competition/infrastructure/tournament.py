from django.db import models
from django.utils.lru_cache import lru_cache

from competition.infrastructure.discipline import Game
from competition.infrastructure.teams import Team


class MatchFormat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    display_name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'match_formats'
        managed = False

    def __str__(self):
        return self.display_name

    @classmethod
    @lru_cache(maxsize=1)
    def get_enabled_match_format(cls):
        return cls.objects.filter(is_active=True).all()


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)
    api_tournament_id = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=30, null=False)
    game = models.ForeignKey(Game, on_delete=False)
    size = models.IntegerField(null=False)
    participant_type = models.CharField(max_length=30, null=False)
    full_name = models.CharField(max_length=80)
    organization = models.CharField(max_length=255)
    website = models.URLField()
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=False)
    online = models.BooleanField(default=True)
    public = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=2, default='JP')
    description = models.CharField(max_length=1500)
    rules = models.CharField(max_length=10000)
    prize = models.CharField(max_length=1500)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='tournaments/')
    match_format = models.ForeignKey(MatchFormat, on_delete=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tournaments'
        managed = False

    def __str__(self):
        return '{}, 開催日: {} ~ {}, ゲーム: {} ({})'.format(
            self.name, self.date_start, self.date_end, self.game.discipline.name, self.game.platform.display_name)


class Stage(models.Model):
    id = models.AutoField(primary_key=True)
    api_stage_id = models.IntegerField(null=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    name = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stages'
        managed = False


class Participate(models.Model):
    id = models.AutoField(primary_key=True)
    api_participate_id = models.CharField(max_length=255, null=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    date_joined = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participates'
        managed = False


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    api_match_id = models.CharField(max_length=255, null=False)
    game = models.ForeignKey(Game, on_delete=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    stage = models.ForeignKey(Stage, on_delete=False)
    group_number = models.IntegerField(null=False)
    round_number = models.IntegerField(null=False)
    match_format = models.ForeignKey(MatchFormat, on_delete=False)
    status = models.CharField(max_length=80, default='pending')
    start_date = models.DateField(default=None)
    start_time = models.TimeField(default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'
        managed = False


class MatchTeam(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    api_opponent_id = models.IntegerField(null=False)
    result = models.IntegerField()
    score = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'match_teams'
        managed = False
