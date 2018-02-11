from enumfields import Enum, EnumField
from django.db import models

from competition.infrastructure.discipline import Game
from competition.infrastructure.teams import Team


class MatchFormat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'match_formats'
        managed = False

    def __str__(self):
        return self.name


class Tournament(models.Model):
    class ParticipantType(Enum):
        TEAM = 'team'
        SINGLE = 'single'

    id = models.AutoField(primary_key=True)
    api_tournament_id = models.IntegerField(null=False)
    name = models.CharField(max_length=30, null=False)
    game = models.ForeignKey(Game, on_delete=False)
    size = models.IntegerField(null=False)
    participant_type = EnumField(ParticipantType)
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
    match_format = models.ForeignKey(MatchFormat, on_delete=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tournaments'
        managed = False


class Stage(models.Model):
    class Type:
        GROUP = 1
        LEAGUE = 2
        SWISS = 3
        SINGLE_ELIMINATION = 4
        DOUBLE_ELIMINATION = 5
        GROUP_BRACKET = 5

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stages'
        managed = False

    def __str__(self):
        return self.name


class Participate(models.Model):
    id = models.AutoField(primary_key=True)
    api_participate_id = models.IntegerField(null=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participates'
        managed = False


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    api_match_id = models.IntegerField(null=False)
    game = models.ForeignKey(Game, on_delete=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    stage_number = models.IntegerField(null=False)
    group_number = models.IntegerField(null=False)
    match_format = models.ForeignKey(MatchFormat, on_delete=False)
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'
        managed = False
