from django.contrib import admin
from .models import Client, Answer, Choice, Question

admin.site.register(Client)
admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(Question)