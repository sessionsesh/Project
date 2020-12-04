from django import forms
from .models import *


class FreeTimeCreateForm(forms.ModelForm):
    class Meta:
        model = FreeTime
        exclude = [
            'owner',
            'task',
        ]

        fields = [
            'beg_datetime',
            'duration'
        ]

        widgets = {
            'beg_datetime': forms.DateTimeInput(format='%d/%m/%Y %H:%M'),
            'duration': forms.NumberInput(),
        }