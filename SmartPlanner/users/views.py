from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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
            messages.success(request, 'Отлично, мы вас запомнили')
            return redirect(redirect_path)
        return render(request, 'register.html', {'form': user_form})
    else:
        user_form = UserRegisterForm()
        return render(request, 'register.html', {'form': user_form})


def login_view(request):
    user_form = UserLoginForm(request.POST or None)
    if user_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),password=password.strip())
        login(request, user)
        messages.success(request, 'Добро пожаловать!')
        return redirect('/mypage') #TODO: перенаправлять в личный кабинет
    return render(request, 'login.html', {'form': user_form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('')

'''
def resetpassword(request): #TODO : сброс забытого пароля
'''
