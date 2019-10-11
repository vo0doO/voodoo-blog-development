from django.contrib import admin
from .models import Client, Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ['created_time', ('author', 'name', 'phone'), ('skolko', 'komu'), ('prosrochky', 'zalogi')]
    list_display = ('created_time', 'author', 'name', 'phone', 'skolko', 'komu', 'prosrochky', 'zalogi')
    list_filter = ('created_time', 'author', 'skolko', 'zalogi', 'prosrochky', 'name', 'phone', 'komu')
    search_fields = ('author', 'name', 'phone')
    ordering = ('created_time',)
    filter_horizontal = ()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass
