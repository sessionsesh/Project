from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as uviews


urlpatterns = [
    path('', include('goals.urls')),
    path('', include('schedule.urls')),
    path('admin/', admin.site.urls),
    path('', uviews.home_view, name='home'),
    path('logout', uviews.logout_view, name='logout'),  # Тут пока ничего нет
    path('register', uviews.register_view, name='register'),
    path('login', uviews.login_view, name='login'),
    path('reset', uviews.reset_password_view, name='reset_password'),
    path('confirm/<key_ref>', uviews.confirm_view, name='confirm'),
    path('change/<key_ref>', uviews.change_password_view, name='change_password_view')
]
