from django import forms
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class UserRegisterForm(forms.ModelForm):
    login = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Повторите пароль',widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = Profile
        fields = ('login',)

    def clean(self, *args, **kwargs): # проверка зависящих друг от друга полей
        cleaned_data = super().clean()
        try:
            user = User.objects.get(username=self.cleaned_data['login'])
            raise forms.ValidationError("Ой! Этот логин уже занят, попробуйте другой")
        except User.DoesNotExist:
            password1 = self.cleaned_data.get("password")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError(
                'Пароли не совпадают!',
                code='password_mismatch',
            )
            users = Profile.objects.filter(email=self.cleaned_data.get("email"))
            if len(users) > 0:
                raise forms.ValidationError("Пользователь с таким email-адресом уже зарегистрирован")
        except KeyError:
            raise forms.ValidationError("Не все поля заполнены")

    def save(self):
        _user = User.objects.create_user(username=self.cleaned_data.get('login'),password=self.cleaned_data.get('password'))
        _user.save()
        user = Profile.objects.create(user=_user, email=self.cleaned_data.get('email'))
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
                #return self.cleaned_data
                return super(UserLoginForm, self).clean(*args, **kwargs)
        except KeyError:
            raise forms.ValidationError("Не все поля заполнены")
        raise forms.ValidationError("Неверно введены логин или пароль")

    def get_user(self):
        return self.authed_user

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