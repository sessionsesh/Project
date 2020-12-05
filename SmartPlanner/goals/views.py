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
            "tasks_counter":tasks_counter}
    return render(request, 'goals_.html', args)


# Если задача выполнена, тогда делает её невыполненной и наоборот
@login_required
def complete_task(request, ID):
    print(request.method)
    task = Task.objects.get(pk=ID)
    if task.is_finished == False:
        task.is_finished = True
    else: 
        task.is_finished = False
    task.save()
    return redirect(f'/goals/{task.goal.id}')



# Goal right from sidebar
@login_required(login_url='login')
def goal_view(request, ID):
    goal = Goal.objects.get(pk=ID)
    goals = list(Goal.objects.filter(owner=request.user))
    
    tasks_counter = {}
    # key is goal id
    # value.1 is goal title
    # value.2 is count of goal's tasks
    for goal_ in goals:
        tasks = list(Task.objects.filter(goal=goal_))
        tasks_counter[goal_.id] = [goal_.title, len(tasks)]

    if request.user == goal.owner:
        tasks = list(Task.objects.filter(goal=goal))
        args = {"goals": goals,
                "goal": goal,
                "tasks": tasks,
                "tasks_counter":tasks_counter,
                }
        return render(request, 'goals.html', args)
    else:
        raise Http404



@login_required(login_url='login')
def add_goal_view(request):
    if request.method == 'POST':
        goal_form = GoalCreateForm(data=request.POST)
        if goal_form.is_valid():
            goal = goal_form.save(request.user)
            return redirect('/goals')
    else:
        goal_form = GoalCreateForm()
    return render(request, 'goal_manipulate.html', {'project_form': goal_form})

@login_required(login_url='login')
def edit_goal_view(request, ID):
    goal = Goal.objects.get(pk=ID)
    if request.method == 'POST':
        goal_form = GoalCreateForm(instance=goal, data=request.POST)
        if goal_form.is_valid():
            goal_form.save(request.user) # doesn't need goal.save() because of custo msave in GoalCreateForm
            return redirect('/goals/{}'.format(ID))
    else:
        goal_form = GoalCreateForm(instance=goal)
    return render(request, 'goal_manipulate.html', {'project_form': goal_form})

from utils.datehelper import *

@login_required(login_url='login')
def delete_goal(request, ID):  # TODO: сделать выдвигающимся окном
    try:
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
    task = Task.objects.get(pk=ID)
    print(ID)
    if request.user == task.goal.owner:
        task.delete()
        return redirect(f'/goals/{task.goal.id}')
    else:
        raise Http404

@login_required(login_url='login')
def add_task_view(request, ID):
    try:
        goal = Goal.objects.get(pk=ID)
        if request.user == goal.owner:
            if request.method == 'POST':
                task_form = TaskCreateForm(data=request.POST)
                if task_form.is_valid():
                    task = task_form.save(commit=False)
                    task.owner = request.user
                    task.goal = goal
                    task.save()
                    return redirect(f'/goals/{task.goal.id}')
                else:
                    messages.error(request,  "Проверьте корректность ссылки! ")
                    tasks = list(Task.objects.filter(goal=goal))
                    args = {"goal": goal, "tasks": tasks}
                    return render(request, 'error.html', args)
           # return redirect("/mygoal/{}".format(str(project.id))) # TODO: на цель пользователя
            else:
                task_form = TaskCreateForm()
                return render(request, 'add_task.html', {'project_form': task_form})
        else:
            raise Http404
    except Goal.DoesNotExist:
        raise Http404  # TODO: Вы слишком далеко забрались!

@login_required(login_url='login')
def edit_task_view(request, ID):
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
            task_form = TaskCreateForm(instance = task)
            return render(request, 'add_task.html', {'project_form': task_form})
    else:
        raise Http404
