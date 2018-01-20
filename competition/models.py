# -*- coding: utf-8 -*-
from django.db import models


class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    logo_url = models.ImageField()
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


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=False)
    name = models.CharField(max_length=255, null=False)
    start_datetime = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schedules'
        managed = True
