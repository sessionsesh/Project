from django.db import models
from django.contrib.auth.models import User
from goals.models import Task

class Day(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # main information
    date = models.DateField(null=True, editable=True, unique=True)
    freetime_count = models.IntegerField(default=0) # counts how many freetime in that day
    feelings = models.TextField(max_length=2000, blank=True)

class FreeTime(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # F
    task = models.OneToOneField(Task, on_delete=models.SET_NULL, null=True) # https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True)

    # main information
    beg_time = models.TimeField(null=True)
    duration = models.IntegerField(null=True)
    
