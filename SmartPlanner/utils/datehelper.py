from datetime import datetime
from calendar import monthrange

# monthrange(year, month)
# Returns weekday of first day of the month and number of days in month, for the specified year and month.

def current_date():
    return datetime.today().strftime("%d/%m/%Y")

def current_day():
    return datetime.today().strftime("%d")

def current_month():
    return datetime.today().strftime("%m")

def current_year():
    return datetime.today().strftime("%Y")

def days_in_month(month, year):
    return monthrange(int(year), int(month))[1]

def first_day_of_week(month, year):
    return monthrange(int(year), int(month))[0]
