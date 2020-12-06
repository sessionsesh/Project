from django import forms
from .models import *


class FreeTimeCreateForm(forms.ModelForm):
    class Meta:
        model = FreeTime
        exclude = [
            'owner',
            'task',
            'day'
        ]

        fields = [
            'beg_time',
            'duration'
        ]

        widgets = {
            'beg_time':forms.TimeInput(),
            'duration': forms.NumberInput()
        }
