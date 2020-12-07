from django.db import models
from users.models import Profile
from django.contrib.auth.models import User

# TODO: сделать первичный ключ строкой из цифр и букв

class Goal(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # main information
    title = models.TextField(max_length=2000, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    # task counters
    completed_task_count = models.IntegerField(default=0)
    task_count = models.IntegerField(default=0)


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, blank=False)

    # main information
    title = models.TextField(blank=True, verbose_name='title')
    url = models.URLField(blank=True, max_length=2000, verbose_name='url')
    duration = models.IntegerField(null=True, verbose_name='duration')

    # const
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='created')
    
    # flags
    is_finished = models.BooleanField(default=False, verbose_name='is_finished')
    in_process = models.BooleanField(default=False, verbose_name='in_process')

