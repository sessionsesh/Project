from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, Http404
from utils.datehelper import *
from .models import *
from .forms import *
from schedule.engine import *

# @login_required
# def free_time_view(request):
#     user_id = request.user.id
#     return render(request, 'free_time.html')

@login_required
def add_free_time(request):
    user_id = request.user.id
    if request.method == 'POST':
        free_time_form = FreeTimeCreateForm(request.POST)
        if free_time_form.is_valid():
            free_time_form.instance.owner = request.user
            free_time_form.save()
            return redirect('/freetime')
        else:
            return render(request, 'error.html')
    else:
        free_time_form = FreeTimeCreateForm()
        free_time_list = list(FreeTime.objects.filter(owner_id=user_id)) # интересно, почему работает с "owner", ведь column в таблице БД имеет value = owner_id
        print("TEMP_DEBUG", free_time_list)
        args = {'free_time_form': free_time_form,
                'free_time_list': free_time_list}
        return render(request, 'free_time.html', args)

@login_required
def delete_free_time(request, ID):
    ft = FreeTime.objects.get(pk=ID)    # ft means freetime
    if request.user == ft.owner:
        ft.delete()
        return redirect('/freetime')
    else:
        raise Http404

@login_required
def calendar_view(request):
    user_id = request.user.id

    month = current_month()
    year = current_year()

    month_tasks = get_all_tasks(month, year, request.user)
    dates = dates_in_month(month, year)

    get_dates_with_tasks(month,year,request.user)
    args = {
        'current_date': current_date(),
        'days_in_current_month': days_in_month(month, year),
        'first_day_of_week': first_day_of_week(month, year),
        'month_tasks': month_tasks,
        'dates': dates
    }
    return render(request, 'calendar.html', args)