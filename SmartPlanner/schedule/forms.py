from django import forms
from .models import *


class FreeTimeCreateForm(forms.ModelForm):
    class Meta:
        model = FreeTimeInterval
        exclude = [
            'owner',
            'task',
            'beg_date'
        ]

        fields = [
            'beg_time',
            'duration'
        ]

        widgets = {
            'beg_time': forms.DateTimeInput(format='%H:%M'),
            'duration': forms.NumberInput(),
        }

        def save(self, user, commit=True):
            goal = super(FreeTimeCreateForm, self).save(commit=False)
            goal.title = self.cleaned_data['title']
            goal.description = self.cleaned_data['description']
            goal.owner = user
            if commit:
                goal.save()
            return goal