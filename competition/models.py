from django.db import models
from django_mysql.models import ListCharField

from account.models import CustomUser as User


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'platforms'
        managed = True

    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    platform = models.ForeignKey(Platform, on_delete=False)
    logo_url = models.URLField()
    home_url = models.URLField()
    is_active = models.BooleanField(default=True)
    date_released = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'games'
        managed = True
        unique_together = ('title', 'platform', )

    def __str__(self):
        return '{} ({})'.format(self.title, self.platform.name)


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
        managed = True

    def __str__(self):
        return self.name


class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    game = models.ForeignKey(Game, on_delete=False)
    stage = models.ForeignKey(Stage, on_delete=False)
    logo_url = models.ImageField('images/logos/competitions/')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1024)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'competitions'
        managed = True

    @classmethod
    def get_competitions(cls):
        return [(c.id, c.name) for c in (Competition.objects.filter(is_active=True)
                                         .order_by('date_created')
                                         .all())]

    @classmethod
    def get_target_game_competitions(cls, game_id):
        return cls.objects.filter(game__id=game_id, is_active=True).order_by('-start_date').all()

    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=255, null=False)
    game = models.ForeignKey(Game, on_delete=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1024)
    is_active = models.BooleanField(default=True)
    logo_url = models.ImageField('images/logos/teams/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        managed = True

    @classmethod
    def get_all_teams_with_organizer(cls):
        teams = cls.objects.all()
        for team in teams:
            team.organizer = Member.objects \
                .values_list('user__nickname', flat=True) \
                .filter(team=team) \
                .filter(is_admin=True).first()
            team.members = ','.join([nickname for nickname in Member.objects
                                    .values_list('user__nickname', flat=True)
                                    .filter(team=team)])
        return teams


class Participate(models.Model):
    id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participates'
        managed = True


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=False)
    round = models.IntegerField(null=False)
    match = ListCharField(base_field=models.IntegerField(), size=2, max_length=(2 * 11))
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'
        managed = True


class MatchResult(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'match_results'
        managed = True


class MemberManager(models.Manager):
    use_for_related_fields = True

    @staticmethod
    def add_member(user, team, is_admin=False):
        member = Member(user=user, team=team, is_admin=is_admin)
        member.save()


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MemberManager()

    class Meta:
        db_table = 'team_members'
        managed = True
        unique_together = (('user', 'team'), ('team', 'is_admin'), )

    @classmethod
    def get_joined_teams(cls, user_id):
        return [(m.team, m.is_admin) for m in
                Member.objects.filter(user_id=user_id).all()]

    @classmethod
    def get_candidate_teams(cls, user_id):
        return [(m.team.id, m.team.teamname) for m in
                Member.objects.exclude(team__id__in=Member.objects.values_list('team__id', flat=True)
                                       .filter(user_id=user_id)
                                       ).all()]
