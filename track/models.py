from django.db import models
from django.contrib.auth.models import User


class Day(models.Model):
    user = models.ForeignKey(User)
    day = models.DateField()
    happiness = models.IntegerField()
    work = models.FloatField()
    case = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=25, null=True)
    state = models.CharField(max_length=2, null=True)
    country = models.CharField(max_length=2, null=True)
    content = models.CharField(max_length=140, null=True)
