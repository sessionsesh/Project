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
    return render(request, 'index.html', {})

def register_view(request):
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
    user_form = UserLoginForm(request.POST or None)
    if user_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),password=password.strip())
        if user is not None:
            login(request, user)
            messages.success(request, 'Добро пожаловать!')
            return redirect('/goals') #TODO: перенаправлять в личный кабинет
    return render(request, 'login.html', {'form': user_form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('')

def reset_password_view(request):
    if request.method=='POST':
        reset_form = PasswordResetForm(request.POST)
        if reset_form.is_valid():
            #reset_form.save()
            messages.success(request, 'Ссылка для смены пароля направлена на вашу почту')
            return redirect('/login')
    else:
        reset_form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': reset_form})

def change_password_view(request, key_ref):
    confirmation = PasswordChangeConfirmation.objects.filter(key_ref = key_ref)
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
        change_form = PasswordChangeForm({'user':user})
    return render(request, 'change_password.html', {'form': change_form})

def confirm_view(request, key_ref):
    confirmation = EmailConfirmation.objects.filter(key_ref=key_ref)
    length = confirmation.count()
    args = {'confirmed': False}
    if length != 0:
        conf = confirmation[0]
        if not conf.key_expired():
            args['confirmed'] = True
            conf.delete()
    return render(request, 'confirm.html',args)

