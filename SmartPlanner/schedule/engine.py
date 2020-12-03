import datetime
from .models import FreeTimeSchedule
from goals.models import Task, Goal
import utils

# UTILS FOR CALENDAR
def get_all_tasks(month, year, user):
        """ Return tasks for month """
        goals = list(Goal.objects.filter(owner=user))
        tasks_list = []
        for goal in goals:
            tasks = list(Task.objects.filter(goal=goal,is_finished=False))
            for task in tasks:
                tasks_list.append(task)
        return tasks_list


def get_dates_with_tasks(month, year, user):
    """ Return dictionary like this: {date_1:[task_1, task_2], etc.} """
    tasks = {}
    month_tasks = get_all_tasks(month, user)
    month_dates = utils.dates_in_month(month, year)
    for date in month_dates:
        tasks_list = []
        for task in month_tasks:
            print(task._meta.get_field('created').value_from_object(task).strftime('%m')) # return value for selected model field
            if date == task._meta.get_field('beg_datetime').value_from_object(task):
                tasks_list.append(task)
        tasks[date] = tasks_list
    return tasks

def create_schedule(user, day):
    free_time = FreeTimeSchedule.objects.filter(user=user)[0]
