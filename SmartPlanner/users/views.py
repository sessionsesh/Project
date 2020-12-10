from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import *
import os


def home_view(request):
    """Отображает домашнюю страницу
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Домашняя страница
    :rtype: django.http.response.HttpResponse
    """
    return render(request, 'index.html', {})


def register_view(request):
    """Отображает страницу регистрации в случае GET запроса. В случае POST проводит успешной регистрацию пользователя и перенаправляет на страницу авторизации
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Страница авторизации
    :rtype: django.http.response.HttpResponse
    :return: Перенаправляет пользователя на страницу регистрации
    :rtype: HttpResponseRedirect
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            redirect_path = '/login'
            return redirect(redirect_path)
    else:
        user_form = UserRegisterForm()
    return render(request, 'register.html', {'form': user_form})


def login_view(request):
    """Отображает страницу авторизации в случае GET запроса. В случае POST проводит авторизацию пользователя и перенаправляет на страницу с целями
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Страница с целями
    :rtype: HttpResponseRedirect
    :return: Перенаправляет пользователя на страницу авторизации
    :rtype: django.http.response.HttpResponse
    """
    user_form = UserLoginForm(request.POST or None)
    if user_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),
                            password=password.strip())
        if user is not None:
            login(request, user)
            messages.success(request, 'Добро пожаловать!')
            return redirect('/goals')  # TODO: перенаправлять в личный кабинет
    return render(request, 'login.html', {'form': user_form})


@login_required(login_url='login')
def logout_view(request):
    """Выходи из аккаунта
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Домашняя страница
    :rtype: HttpResponseRedirect
    """
    logout(request)
    return redirect('')


def reset_password_view(request):
    """Отображает страницу для сброса пароля. Отправляет письмо с ссылкой для сброса пароля и перенаправляет на страницу авторизации
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest

    :return: Страница авторизации
    :rtype: HttpResponseRedirect

    :return: Страница сброса пароля
    :rtype: django.http.response.HttpResponse
    """
    if request.method == 'POST':
        reset_form = PasswordResetForm(request.POST)
        if reset_form.is_valid():
            #reset_form.save()
            messages.success(
                request, 'Ссылка для смены пароля направлена на вашу почту')
            return redirect('/login')
    else:
        reset_form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': reset_form})


def change_password_view(request, key_ref):
    """Отображает страницу для восстановления пароля. При успешной смене перенаправляет на страницу авторизации
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest

    :parameter key_ref: Уникальный ключ для подтверждения сброса пароля
    :type key_ref: int

    :return: Страница авторизации
    :rtype: HttpResponseRedirect

    :return: Страница сброса пароля
    :rtype: django.http.response.HttpResponse
    """
    confirmation = PasswordChangeConfirmation.objects.filter(key_ref=key_ref)
    length = confirmation.count()
    if length == 0:
        raise Http404
    user = confirmation[0].user
    if request.method == 'POST':
        change_form = PasswordChangeForm(request.POST)
        if change_form.is_valid():
            change_form.save(user=user)
            confirmation[0].confirm()
            # so that user does not get logged out, not working as of now.
            # TODO
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен')
            return redirect('/login')
    else:
        change_form = PasswordChangeForm({'user': user})
    return render(request, 'change_password.html', {'form': change_form})


def confirm_view(request, key_ref):
    """Проверяет, истек ли срок годности ключа или нет и возвращает страницу подтверждения
    
    :parameter request: Запрос пользователя
    :type request: django.core.handlers.wsgi.WSGIRequest

    :parameter key_ref: Уникальный ключ для подтверждения сброса пароля
    :type key_ref: int

    :return: Страница подтверждения
    :rtype: django.http.response.HttpResponse
    """

    confirmation = EmailConfirmation.objects.filter(key_ref=key_ref)
    length = confirmation.count()
    args = {'confirmed': False}
    if length != 0:
        conf = confirmation[0]
        if not conf.key_expired():
            args['confirmed'] = True
            conf.delete()
    return render(request, 'confirm.html', args)
