import datetime
from .models import FreeTimeInterval
from goals.models import Task, Goal
from utils import datehelper


# TODO: Изменить функции с перспективы FreeTime
# То есть идём по списку из элементов FreeTime, если beg_datetime == iteration.current_datetime

# UTILS FOR CALENDAR
def get_all_tasks(user):
    """ Return all tasks """
    free_time_list = FreeTimeInterval.objects.filter(owner=user)
    tasks_list = []
    for each in free_time_list:
        if each.task:
            tasks_list.append(each.task)
    return tasks_list


def get_tasks_for_n_days(first_date, n, user):
    """ Return tasks for n days from selected date """
    free_time_list = FreeTimeInterval.objects.filter(owner=user)
    tasks_list = []
    days = 0
    for each in free_time_list:
        if each.beg_datetime.date() >= first_date and each.task is not None and days <= n:
            tasks_list.append(each.task)
    return tasks_list


def get_dates_with_tasks(month, year, user):
    """ Return dictionary like this: {date_1:[task_1, task_2], etc.} """
    tasks = {}
    all_tasks = get_all_tasks(user)
    month_dates = datehelper.dates_in_month(month, year)
    for date in month_dates:
        tasks_list = []
        for task in all_tasks:
            if date == task._meta.get_field('beg_datetime').value_from_object(task):
                tasks_list.append(task)
        tasks[date] = tasks_list
    return tasks

