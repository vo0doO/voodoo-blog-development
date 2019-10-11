from django.contrib import admin

# Register your models here.
from .models import Channel, Tag, Post, Image, Log


class PostInline(admin.TabularInline):
    model = Post


@admin.register(Channel)
class AdminChannel(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'created_date', 'like',)
    list_filter = ('created_date', 'like',)
    inlines = [PostInline]


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'created_date', 'like',)
    list_filter = ('created_date', 'like',)
    inline = [PostInline]


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    fieldsets = (
        ('Действия', {'fields': ('author', 'created_date', 'pub_date',)}),
        ('Содержание', {'fields': ('title', 'text', 'img',)}),
        ("Связи", {'fields': ('channel', 'tags',)}),
        ("Свойства", {'fields': ('status', 'url', 'slug',)}),
        )
    search_fields = ('title', 'text',)
    ordering = ('-status',)
    list_display = ('title', 'channel', 'display_tag', 'created_date', 'display_image',  'status', 'author')
    list_filter = ('channel', 'tags', 'status', 'created_date', 'pub_date', 'rewrite_date',)
    filter_horizontal = ()


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ('created_time', 'id',)
    list_filter = ('created_time',)



@admin.register(Log)
class AdminLog(admin.ModelAdmin):
    list_display = ('text', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('text',)
    ordering = ('created_at',)
    filter_horizontal = ()