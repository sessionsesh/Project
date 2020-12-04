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
            'end_datetime'
        ]

        widgets = {
            'beg_datetime': forms.DateTimeInput(format='%d/%m/%Y %H:%M'),
            'end_datetime': forms.DateTimeInput(format='%d/%m/%Y %H:%M'),
        }