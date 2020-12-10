from utils.datehelper import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, Http404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import *
from .forms import *
import users

# Sidebar and it's content
# Goals in sidebar


@login_required(login_url='login')
def goals_view(request):
    """Отображает страницу с целями
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest

    :return: Страница с целями
    :rtype: django.http.response.HttpResponse
    """
    user_id = request.user.id

    # test user models in goals app
    # print(users.models.User.objects.get(pk=user_id).get_profile())

    goals = list(Goal.objects.filter(owner=request.user))
    if len(goals) == 0:
        goals = []

    tasks_counter = {}
    # key is goal id
    # value.1 is goal title
    # value.2 is count of goal's tasks
    for goal in goals:
        tasks = list(Task.objects.filter(goal=goal))
        tasks_counter[goal.id] = [goal.title, len(tasks)]

    # log
    print("LOG: ", tasks_counter)

    args = {"goals": goals,
            "tasks_counter": tasks_counter}
    return render(request, 'goals_.html', args)


# Если задача выполнена, делает её невыполненной и наоборот
@login_required
def complete_task(request, ID):
    """Меняет значение поля is_finished задачи на True, если оно равно False и наоборот
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :parameter ID: Первичный ключ задачи
    :type ID: Int

    :return: Страница цели, которой пренадлежит задача
    :rtype: HttpResponseRedirect
    """
    if request.method == 'GET':
        task = Task.objects.get(pk=ID)
        if task.is_finished == False:
            task.is_finished = True
        else:
            task.is_finished = False
        task.save()
        return redirect(f'/goals/{task.goal.id}')
    else:
        return render('error.html')


# Goal right from sidebar
@login_required(login_url='login')
def goal_view(request, ID):
    """Отображает цель и её задачи
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :parameter ID: Первичный ключ цели
    :type ID: Int

    :return: Страница цели с задачами
    :rtype: HttpResponse
    """
    goal = Goal.objects.get(pk=ID)
    goals = list(Goal.objects.filter(owner=request.user))

    tasks_counter = {}
    # key is goal id
    # value.1 is goal title
    # value.2 is count of goal's tasks
    for each_goal in goals:
        tasks = Task.objects.filter(goal=each_goal, is_finished=False)
        tasks_counter[each_goal.id] = [each_goal.title, len(tasks)]

    if request.user == goal.owner:
        completed_tasks = Task.objects.filter(goal=goal, is_finished=True)
        uncompleted_tasks = Task.objects.filter(goal=goal, is_finished=False)
        args = {"goals": goals,
                "goal": goal,
                "completed_tasks": completed_tasks,
                "uncompleted_tasks": uncompleted_tasks,
                "tasks_counter": tasks_counter,
                }
        return render(request, 'goals.html', args)
    else:
        raise Http404


@login_required(login_url='login')
def add_goal_view(request):
    """Добавляет новую цель в базу данных и отображает выполненные изменения
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest

    :return: Страница с целями
    :rtype: HttpResponseRedirect
    """
    if request.method == 'POST':
        """
        test test test
        ===============
        """
        goal_form = GoalCreateForm(data=request.POST)
        if goal_form.is_valid():
            goal = goal_form.save(request.user)
            return redirect('/goals')
    else:
        goal_form = GoalCreateForm()
    return render(request, 'goal_manipulate.html', {'project_form': goal_form})


@login_required(login_url='login')
def edit_goal_view(request, ID):
    """Изменяет поля цели, сохраняет изменения в базу данных и отображает изменения пользователю
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :parameter ID: Первичный ключ цели
    :type ID: Int

    :return: Страница с целью и её содержимым
    :rtype: HttpResponseRedirect
    """
    goal = Goal.objects.get(pk=ID)
    if request.method == 'POST':
        goal_form = GoalCreateForm(instance=goal, data=request.POST)
        if goal_form.is_valid():
            # doesn't need goal.save() because of custo msave in GoalCreateForm
            goal_form.save(request.user)
            return redirect('/goals/{}'.format(ID))
    else:
        goal_form = GoalCreateForm(instance=goal)
    return render(request, 'goal_manipulate.html', {'project_form': goal_form})


@login_required(login_url='login')
def delete_goal(request, ID):  # TODO: сделать выдвигающимся окном
    """Удаляет цель из базы данных и отображает изменения пользователю
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :parameter ID: Первичный ключ цели
    :type ID: Int

    :return: Страница с целями
    :rtype: HttpResponseRedirect
    """
    try:
        if request.method == 'GET':
            goal = Goal.objects.get(pk=ID)
            if request.user == goal.owner:
                goal.delete()
                return redirect('/goals')
            else:
                raise Http404
    except Goal.DoesNotExist:
        raise Http404


@login_required(login_url='login')
def delete_task(request, ID):
    """Удаляет задачу из базы данных и отображает изменения пользователю
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :parameter ID: Первичный ключ задачи
    :type ID: Int

    :return: Страница с целью, которой принадлежала задача
    :rtype: HttpResponseRedirect
    """
    if request.method == 'GET':
        task = Task.objects.get(pk=ID)
        print(ID)
        if request.user == task.goal.owner:
            task.delete()
            return redirect(f'/goals/{task.goal.id}')
        else:
            raise Http404


@login_required(login_url='login')
def add_task_view(request, ID):
    """Добавляет задачу в базу данных, сохраняет изменения и отображает их пользователю
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :parameter ID: Первичный ключ задачи
    :type ID: Int

    :return: Страница с целью, которой принадлежит задача
    :rtype: HttpResponseRedirect
    """
    try:
        goal = Goal.objects.get(pk=ID)
        if request.user == goal.owner:
            if request.method == 'POST':
                task_form = TaskCreateForm(data=request.POST)
                print('DEBUG_BEFORE_VALID')
                if task_form.is_valid():
                    print('DEBUG_IS_VALID')
                    task = task_form.save(commit=False)
                    task.owner = request.user
                    task.goal = goal
                    task.save()

                    # change task count in goal
                    goal.task_count += 1
                    goal.save()
                    return redirect(f'/goals/{task.goal.id}')
                else:
                    print('DEBUG_ISNOT_VALID')
                    messages.error(request,  "Проверьте корректность ссылки! ")
                    tasks = list(Task.objects.filter(goal=goal))
                    args = {"goal": goal, "tasks": tasks}
                    return render(request, 'error.html', args)
            else:
                task_form = TaskCreateForm()
                return render(request, 'add_task.html', {'project_form': task_form})
        else:
            raise Http404
    except Goal.DoesNotExist:
        raise Http404  # TODO: Вы слишком далеко забрались!


@login_required(login_url='login')
def edit_task_view(request, ID):
    """Отображает страницу с изменением содержания задачи в случае GET запроса. Изменяет содержимое задачи и сохрняет изменения в базу данных в случае POST запроса  
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :parameter ID: Первичный ключ задачи
    :type ID: Int

    :return: Страница с целью, которой принадлежит задача
    :rtype: HttpResponseRedirect
    """
    task = Task.objects.get(pk=ID)
    if request.user == task.goal.owner:
        if request.method == 'POST':
            task_form = TaskCreateForm(instance=task, data=request.POST)
            if task_form.is_valid():
                task_form.save(commit=False)
                task.save()
                return redirect('/goals')
        # return redirect("/mygoal/{}".format(str(project.id))) # TODO: на цель пользователя
        else:
            task_form = TaskCreateForm(instance=task)
            return render(request, 'add_task.html', {'project_form': task_form})
    else:
        raise Http404
