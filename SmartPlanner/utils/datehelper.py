""" 
Простой API для взаимодействия с базовым модулем datetime языка python

"""

from datetime import datetime as dt
import datetime
from calendar import monthrange



def current_date():
    """
    :return: Возвращает текущую дату и время
    :rtype: datetime.datetime
    """
    return dt.today()

def current_day():
    """
    :return: Возвращает текущий день
    :rtype: datetime.datetime
    """
    return dt.today().day

def current_month():
    """
    :return: Возвращает текущий месяц
    :rtype: datetime.datetime
    """
    return dt.today().month

def current_year():
    """
    :return: Возвращает текущий год
    :rtype: datetime.datetime
    """
    return dt.today().year

def days_in_month(month, year):
    """
    :parameter month: Месяц
    :type month: Int
    :parameter month: Год
    :type month: Int
    :return: Возвращает количество дней в месяце
    :rtype: int
    """
    return monthrange(int(year), int(month))[1]

def first_day_of_week(month, year):
    """
    :parameter month: Месяц
    :type month: Int
    :parameter month: Год
    :type month: Int
    :return: Возвращает первый день недели месяца
    :rtype: int
    """
    weekday_digit = monthrange(int(year), int(month))[0]
    dict_digit_day = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    return dict_digit_day[weekday_digit]
    
def dates_in_month(month, year):
    """
    Возвращает список дней в месяце

    :parameter month: Месяц
    :type month: Int
    :parameter month: Год
    :type month: Int
    :return: Список дней
    :rtype: list
    """
    days_counter = days_in_month(month, year)
    days = [datetime.date(year, month, day) for day in range(1, days_counter + 1)]
    return days

