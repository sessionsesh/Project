from django.urls import path
from goals import views as gviews
from . import views

app_name = 'goals'
urlpatterns = [
    path('goals/', gviews.goals_view, name = 'goals_view'),
    path('add', gviews.add_goal_view, name = 'add_goal'),
    path('goals/<ID>', gviews.goal_view, name='goal_view'),
    path('edit/<ID>', gviews.edit_goal_view, name='edit_goal'),
    path('delete/<ID>', gviews.delete_goal, name = 'delete_goal'),
    path('add/<ID>', gviews.add_task_view, name = 'add_task'),
    path('delete_task/<ID>', gviews.delete_task, name = 'delete_task'),
    path('show_tasks/<ID>', gviews.delete_goal, name = 'tasks_view'),
    path('calendar', gviews.calendar_view, name = 'calendar_view'),
]