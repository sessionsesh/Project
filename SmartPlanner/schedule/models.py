from django.db import models
from django.contrib.auth.models import User
from goals.models import Task

class FreeTimeInterval(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    beg_date = models.DateField(null = False, verbose_name='begin_date')
    beg_time = models.TimeField(null=True, editable= True, verbose_name='begin_time')
    duration = models.IntegerField(null=True, verbose_name='duration')
    task = models.OneToOneField(Task, on_delete=models.SET_NULL, null=True) # https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models


