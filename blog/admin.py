from django.contrib import admin
from .models import Client, Answer, Question, Choice

admin.site.register(Client)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Choice)