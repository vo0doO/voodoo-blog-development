from django import forms
from .models import Answer, Choice, Question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('skolko', 'komu')
