from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as uviews


urlpatterns = [
    path('', include('goals.urls')),
    path('admin/', admin.site.urls),
    path('', uviews.home_view, name='home'),
    path('logout', uviews.logout_view, name='logout'),  # Тут пока ничего нет
    path('register', uviews.register_view, name='register'),
    path('login', uviews.login_view, name='login'),
    path('reset', uviews.reset_password_view, name='reset_password'),

    # path('mypage', gviews.main_view, name = 'my goals'),
    # path('add', gviews.add_goal_view, name = 'add_goal'),
    # path('view/<ID>', gviews.goal_view, name='goal_view'),
    # path('edit/<ID>', gviews.edit_goal_view, name='edit_goal'),
    # path('delete/<ID>', gviews.delete_goal, name = 'delete_goal'),
    # path('add/<ID>', gviews.add_task_view, name = 'add_task'),
    # path('delete_task/<ID>', gviews.delete_task, name = 'delete_task'),
    # path('show_tasks/<ID>', gviews.delete_goal, name = 'tasks_view'),
    # path('calendar', gviews.calendar_view, name = 'calendar_view'),
    # path('home',  gviews.home_view, name = 'home_view'),
    # path('tasks', gviews.tasks_view, name = 'tasks_view')
]
