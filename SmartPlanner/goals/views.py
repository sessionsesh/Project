from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, Http404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import *
from .forms import *

@login_required(login_url='login')
def main_view(request):
    user_id = request.user.id
    goals = list(Goal.objects.filter(owner = request.user))
    print(goals)
    if len(goals)==0:
        goals = None
    args = {"dict_": goals}
    return render(request, 'main.html', args)


@login_required
def delete_task(request, ID):
    task = Task.objects.get(pk=ID)
    print(ID)
    if request.user == task.goal.owner:
        task.delete()
        return redirect('/mypage')
    else:
        raise Http404


@login_required
def goal_view(request, ID):
    goal = Goal.objects.get(pk=ID)
    if request.user == goal.owner:
        tasks = list(Task.objects.filter(goal=goal))
        args = {"goal":goal,"tasks": tasks}
        return render(request, 'goal_view.html', args)
    else:
        raise Http404

@login_required
def add_goal_view(request):
    if request.method == 'POST':
        goal_form = GoalCreateForm(data=request.POST)
        if goal_form.is_valid():
            goal = goal_form.save(request.user)
            return redirect('/mypage')
    else:
        goal_form = GoalCreateForm()
    return render(request, 'add_goal.html', {'project_form': goal_form})


@login_required
def delete_goal(request, ID): # TODO: сделать выдвигающимся окном
    try:
        goal = Goal.objects.get(pk=ID)
        if request.user == goal.owner:
            goal.delete()
            return redirect('/mypage')
        else:
            raise Http404
    except Goal.DoesNotExist:
        raise Http404

@login_required
def tasks_view(request, ID):
    pass


@login_required
def add_task_view(request, ID):
    try:
        goal = Goal.objects.get(pk=ID)
        if request.user == goal.owner:
            if request.method== 'POST':
                task_form = TaskCreateForm(data=request.POST)
                if task_form.is_valid():
                    task = task_form.save(commit=False)
                    task.owner = request.user
                    task.goal = goal
                    task.save()
                    return redirect('/mypage')
                else:
                    messages.error(request,  "Проверьте корректность ссылки! ")
                    return render(request, 'add_task.html', {'project_form': task_form})
           # return redirect("/mygoal/{}".format(str(project.id))) # TODO: на цель пользователя
            else:
                task_form = TaskCreateForm()
                return render(request, 'add_task.html', {'project_form': task_form})
        else:
            raise Http404
    except Goal.DoesNotExist:
        raise Http404 # TODO: Вы слишком далеко забрались!

@login_required
def edit_goal_view(request, ID):
    pass

@login_required
def calendar_view(request):
    return render(request, 'calendar.html')
