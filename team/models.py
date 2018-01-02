from django.db import models
from django.utils.lru_cache import lru_cache

from account.models import CustomUser as User


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=255, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1024)
    is_active = models.BooleanField(default=True)
    logo_url = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        managed = True

    @classmethod
    def get_all_teams_with_organizer(cls):
        teams = cls.objects.all()
        for team in teams:
            team.organizer = Member.objects\
                .values_list('user__nickname', flat=True)\
                .filter(team=team)\
                .filter(is_admin=True).first()
            team.members = ','.join([nickname for nickname in Member.objects
                                    .values_list('user__nickname', flat=True)
                                    .filter(team=team)])
        return teams


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
