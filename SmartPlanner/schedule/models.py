from django.db import models
from django.contrib.auth.models import User
from goals.models import Task

class FreeTimeSchedule(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    free_time = models.JSONField()


class DaySchedule(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='date')
    tasks = models.ManyToManyField(Task)
