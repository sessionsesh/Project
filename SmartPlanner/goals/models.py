from django.db import models
from users.models import Profile
from django.contrib.auth.models import User

# TODO: сделать первичный ключ строкой из цифр и букв

class Goal(models.Model): # цель
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=2000, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_reached = models.BooleanField(default=False, verbose_name='is reached?')
    end_date = models.DateField(blank=True, null=True, verbose_name='end_date')
    progress = models.IntegerField(default=0)


    # tag = models.SlugField() # тут хранится url, быть или не быть ?
    # можно сделать Generic Relation для ссылок на разные вещи (статьи, фильмы, курсы)

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    url = models.URLField(blank=True, max_length=2000, verbose_name='url_link')
    title = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='date_created', editable=False)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, blank=False)
    is_finished = models.BooleanField(verbose_name='task_is_finished', default=False)
    in_process = models.BooleanField(verbose_name='task_in_process', default=False)
    duration = models.IntegerField(null=True ,verbose_name='duration')
