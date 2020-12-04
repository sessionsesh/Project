from django.db import models
from django.contrib.auth.models import User
from goals.models import Task

class FreeTime(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    beg_datetime = models.DateTimeField(null=True, editable= True, verbose_name='begin_datetime')
    end_datetime = models.DateTimeField(null=True, editable= True, verbose_name='end_datetime')
    task = models.OneToOneField(Task, on_delete=models.SET_NULL, null=True) # https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
