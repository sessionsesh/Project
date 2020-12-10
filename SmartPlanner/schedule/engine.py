import datetime
from .models import FreeTime
from goals.models import Task, Goal
from utils import datehelper


# TODO: Изменить функции с перспективы FreeTime
# То есть идём по списку из элементов FreeTime, если beg_datetime == iteration.current_datetime

# UTILS FOR CALENDAR
def get_all_tasks(user):
    """Возвращает список задач пользователя, которые не выполняются и не завершены
    
    :parameter user: Объект пользователя
    :type request: User
    :return: Список всех задач пользователя
    :rtype: list
    """
    free_time_list = FreeTime.objects.filter(owner=user)
    tasks_list = []
    for each in free_time_list:
        tasks_list.append(each.task)
    return tasks_list


def get_tasks_for_n_days(first_date, n, user):
    """Возвращает список задач пользователя с выбранной даты до дня n
    
    :parameter first_date: Дата, с которой начинается отсчёт
    :type first_date: datetime.date

    :parameter n: Количество дней
    :type n: int

    :parameter user: Объект пользователя
    :type request: User

    :return: Список задач
    :rtype: list
    """

    free_time_list = FreeTime.objects.filter(owner=user)
    tasks_list = []
    counter = 0
    for each in free_time_list:
        if each.beg_datetime.date() >= first_date and each.task is not None and counter <= n:
            counter += 1
            tasks_list.append(each.task)
    return tasks_list

def get_dates_with_tasks(month, year, user):
    """Возвращает словарь дат и связанных с ними задач в выбранном месяце года
    
    :parameter month: Месяц
    :type month: int

    :parameter year: Год
    :type n: int

    :parameter user: Объект пользователя
    :type request: User

    :return: Словарь вида {date_1:[task_1, task_2], etc.}
    :rtype: dict
    """

    tasks = {}
    all_tasks = get_all_tasks(user)
    month_dates = datehelper.dates_in_month(month, year)
    for date in month_dates:
        tasks_list = []
        for task in all_tasks:
            print(task._meta.get_field('created').value_from_object(task).strftime('%m')) # return value for selected model field
            if date == task._meta.get_field('beg_datetime').value_from_object(task):
                tasks_list.append(task)
        tasks[date] = tasks_list
    return tasks

