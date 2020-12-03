from django import forms
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from .models import Profile, EmailConfirmation, PasswordChangeConfirmation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError

class UserRegisterForm(forms.Form):
    login = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_2 = forms.CharField(label='Повторите пароль',widget=forms.TextInput(attrs={'class':'form-control'}))


    def clean(self, *args, **kwargs): # проверка зависящих друг от друга полей
        cleaned_data = super().clean()
        try:
            user = User.objects.get(username=self.cleaned_data['login'])
            raise forms.ValidationError("Ой! Этот логин уже занят, попробуйте другой")
        except User.DoesNotExist:
            password1 = self.cleaned_data.get("password")
            password_2 = self.cleaned_data.get("password_2")
            if password1 and password_2 and password1 != password_2:
                print('Go fuck yourself')
                raise forms.ValidationError('Пароли не совпадают!')
            users = User.objects.filter(email=self.cleaned_data["email"])
            if users.count() > 0:
                raise forms.ValidationError("Пользователь с таким email-адресом уже зарегистрирован")
        except KeyError:
            raise forms.ValidationError("Не все поля заполнены")

    def save(self):
        email = self.cleaned_data.get('email')
        _user = User.objects.create_user(username=self.cleaned_data.get('login'),password=self.cleaned_data.get('password'), email=email)
        _user.save()
        user = Profile.objects.create(user=_user, verified=False)
        email = EmailConfirmation.objects.create(user=user, email_adress=email)  # создаем и сразу сохраняем
        email.send()
        user.save()
        return user



class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus','class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password_login','class':'form-control'}))

    def clean(self, *args, **kwargs): # проверка зависящих друг от друга полей
        cleaned_data = super().clean()
        try:
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            try:
                self.authed_user = authenticate(username=username, password = password)
            except ValueError:
                self.authed_user = None
            if self.authed_user:
                confs = EmailConfirmation.objects.filter(email_adress = self.authed_user.email)
                if confs.count()>0:
                    raise forms.ValidationError("Подтвердите, пожалуйста, адрес электронной почты")
                #return self.cleaned_data
                return super(UserLoginForm, self).clean(*args, **kwargs)
        except KeyError:
            raise forms.ValidationError("Не все поля заполнены")
        raise forms.ValidationError("Неверно введены логин или пароль")

    def get_user(self):
        return self.authed_user

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label = 'email-адрес', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}), error_messages={'invalid': 'Некорректный адрес'})
    login = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        try:
            email = cleaned_data.get('email')
            login = cleaned_data.get('login')
            users = User.objects.filter(email=email, username=login)
            if users.count() == 0:
                raise forms.ValidationError("Пользователь с такими данными не найден")
            user = users[0]
            print('Отправлено')
            confirmation = PasswordChangeConfirmation.objects.create(user = user)
            confirmation.send()
            print('Отправлено')
        except KeyError:
            raise forms.ValidationError("Не все поля заполнены")
        except IntegrityError:
            raise forms.ValidationError("Запрос на смену пароля уже был создан, проверьте почту")



class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    password_2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'off'}))
    #TODO: добавить проверку на надежность


    def clean(self, *args, **kwargs): # проверка зависящих друг от друга полей
        cleaned_data = super().clean()
        try:
            password_1 = cleaned_data.get('password')
            password_2 = cleaned_data.get('password_2')
            if password_1 and password_2 and password_1 != password_2:
                raise forms.ValidationError('Пароли не совпадают!')
            return super(PasswordChangeForm, self).clean(*args, **kwargs)
        except KeyError:
            raise forms.ValidationError("Не все поля заполнены")
        raise forms.ValidationError("Неверно введены логин или пароль")

    def save(self, user, commit=True):
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user

'''

class DisconnectForm(forms.Form):
    account = forms.ModelChoiceField(queryset=SocialAccount.objects.none(),
                                     widget=forms.RadioSelect,
                                     required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.accounts = SocialAccount.objects.filter(user=self.request.user)
        super(DisconnectForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = self.accounts

    def clean(self):
        cleaned_data = super(DisconnectForm, self).clean()
        account = cleaned_data.get('account')
        if account:
            get_adapter(self.request).validate_disconnect(
                account,
                self.accounts)
        return cleaned_data

    def save(self):
        account = self.cleaned_data['account']
        account.delete()
        signals.social_account_removed.send(sender=SocialAccount,
                                            request=self.request,
                                            socialaccount=account)'''