from django import forms
from .models import Answer, Choice, Question


class AnswerForm(forms.ModelForm):
    choices = forms.ModelMultipleChoiceField(queryset=Choice.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Answer
        fields = ('skolko', 'komu')
