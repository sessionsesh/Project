from datetime import datetime as dt
import datetime
from calendar import monthrange

# DATETIME API
def current_date():
    return dt.today()

def current_day():
    return dt.today().day

def current_month():
    return dt.today().month

def current_year():
    return dt.today().year

def days_in_month(month, year):
    return monthrange(int(year), int(month))[1]

def first_day_of_week(month, year):
    """ Retrun first weekday of month """
    weekday_digit = monthrange(int(year), int(month))[0]
    dict_digit_day = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    return dict_digit_day[weekday_digit]
    
def dates_in_month(month, year):
    """ Retrun list of dates in month """
    days_counter = days_in_month(month, year)
    days = [datetime.date(year, month, day) for day in range(1, days_counter + 1)]
    return days

