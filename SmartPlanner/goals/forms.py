from django import forms
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from goals import parser

class GoalCreateForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = (
            'owner',
            'is_reached',
            'progress',
            'created',
            'end_date',
        )

        fields = (
            'title',
            'description',
        )
        widgets = {
            'title': forms.Textarea(attrs={'cols': 100, 'rows': 1, 'class':'goal-title', 'placeholder':'Название'}),
            'description': forms.Textarea(attrs={'cols': 100, 'rows': 20, 'class':'goal-description', 'placeholder':'Описание'}),
          #  'end_date': forms.DateInput(attrs={'class': 'datefield'}), # TODO: добавить автоматический расчет
        }

    def save(self, user, commit=True):
        goal = super(GoalCreateForm, self).save(commit=False)
        goal.title = self.cleaned_data['title']
        goal.description = self.cleaned_data['description']
        goal.owner = user
        if commit:
            goal.save()
        return goal


class GoalModelForm(forms.ModelForm):
    name = forms.CharField(label='Название',
                           widget=forms.TextInput( attrs={'class': 'form-control'}))
    #created = forms.DateField(widget=forms.HiddenInput())
    description = forms.CharField(widget=forms.HiddenInput())
    progress = forms.CharField(widget=forms.HiddenInput())

    class Meta():
        model = Goal
        fields = ('title', 'description','progress')

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('url', 'title')
        exclude = {'owner',
                   'created',
                   'goal',
                   'is_finihed'}
        widgets = {
            'url': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'title': forms.Textarea(attrs={'cols': 80, 'rows': 20}),}

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        title = cleaned_data.get('title')
        if url!='':
            if parser.parse(url):
                return super(TaskCreateForm, self).clean(*args, **kwargs)
            else:
                print("Check url")
                raise forms.ValidationError("Проверьте ссылку") # TODO: добавить некорректность ссылки как ошибку
        elif title=='':
            print("No title")
            raise forms.ValidationError("Название или ссылка на ресурс должны быть обязательно")
        return super(TaskCreateForm, self).clean(*args, **kwargs)

