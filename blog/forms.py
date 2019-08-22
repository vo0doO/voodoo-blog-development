from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('step_1', 'step_2', 'step_3', 'step_4', 'step_5', 'step_6',)