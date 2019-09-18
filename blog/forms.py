from django import forms
from .models import Answer
from phonenumber_field.formfields import PhoneNumberField


class AnswerForm(forms.ModelForm):
    phone = PhoneNumberField

    class Meta:

        model = Answer
        fields = (
            'skolko',
            'komu',
            'prosrochky',
            'zalogi',
            'name',
            'phone',
        )
