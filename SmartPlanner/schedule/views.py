from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, Http404
from utils.datehelper import *
from .models import *
from .forms import *
from schedule.engine import *
import datetime


@login_required
def schedule_generator(request):
    ''' Просто добавляет задачи в FreeTime если их длительность <= длительности FreeTime '''
    ''' Ставится метка in_process = True '''
    freetime = FreeTime.objects.filter(task=None)
    tasks_to_do = Task.objects.filter(in_process=False, is_finished=False)
    for task in tasks_to_do:
        for ft in freetime:
            if ft.task is None:  # так как задача на этот FreeTime может быть поставлена ранее в этом цикле
                if ft.duration >= task.duration:
                    task.in_process = True
                    task.save()
                    ft.task = task
                    ft.save()
                    break
    return redirect('/calendar')


@login_required
def add_free_time(request):
    user_id = request.user.id
    if request.method == 'POST':
        free_time_form = FreeTimeCreateForm(request.POST)
        if free_time_form.is_valid():
            # Ищем в днях запись с датой из POST запроса
            day = Day.objects.filter(date=request.POST['day'])

            # Если такой записи нет, то создаем и сохраняем
            if len(day) == 0:
                day = Day()
                day.owner = request.user
                day.date = datetime.datetime.strptime(
                    request.POST['day'], '%Y-%m-%d').date()
                day.freetime_count += 1
                day.save()
            else:
                day = day.first()
                day.freetime_count += 1
                day.save()

            # Сохранение новой записи FreeTime
            freetime = free_time_form.save(commit=False)
            freetime.owner = request.user
            freetime.day = day

            task_id = request.POST['task']

            if task_id:
                ''' Если пользователем была выбрана задача из списка, поставить её на выполнение '''
                user_task = Task.objects.get(pk=task_id)
                user_task.in_process = True
                user_task.save()
                freetime.task = user_task

            freetime.save()
            return redirect('/calendar')
        else:
            raise Http404
    else:
        raise Http404


@login_required
def delete_free_time(request, ID):
    ft = FreeTime.objects.get(pk=ID)    # ft means freetime
    if request.user == ft.owner:
        # Уменьшаем количество задач в дне, который был связан с FreeTime
        ft.day.freetime_count -= 1
        ft.day.save()

        # Задача теперь не находится в процессе выполнения
        if ft.task is not None:
            ft.task.in_process = False
            ft.task.save()

        # Удаление FreeTime
        ft.delete()
        return redirect('/calendar')
    else:
        raise Http404


@login_required
def calendar_view(request):
    user_id = request.user.id

    month = current_month()
    year = current_year()

    month_tasks = get_all_tasks(request.user)
    dates = dates_in_month(month, year)

    # TODO: подумать, как сделать так, чтобы в модальной форме для каждого дня оторажались задачи именно на этот день

    # Список всех FreeTime отдельного пользователя
    free_time_list = FreeTime.objects.filter(owner_id=user_id)

    # Словарь вида {datetime.date:[FreeTime.object.0, FreeTime.object.1]}
    date_freetime_dict = {}
    for ft in free_time_list:
        date_freetime_dict.setdefault(ft.day.date, []).append(ft)
        ''' Если список есть в словаре по этому ключу, и добавь к нему ft.
            Иначе создай список '''

    args = {
        'current_date': current_date(),
        'days_in_current_month': days_in_month(month, year),
        'first_day_of_week': first_day_of_week(month, year),
        'month_tasks': month_tasks,
        'dates': dates,
        'date_freetime_dict': date_freetime_dict
    }
    return render(request, 'calendar.html', args)


@login_required
def get_tasks(request):
    ''' Возвращает список задач пользователя, которые не выполняются и не завершены'''
    if request.method == 'GET':
        user_tasks = Task.objects.filter(owner=request.user.id,
                                         is_finished=False,
                                         in_process=False)
        args = {'tasks': user_tasks}
        return render(request, "tasks_for_choose.html", args)
    else:
        raise Http404
