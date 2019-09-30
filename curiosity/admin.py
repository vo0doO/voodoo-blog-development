from django.contrib import admin

# Register your models here.
from .models import Channel, Tag, Post


class PostInline(admin.TabularInline):
    model = Post

@admin.register(Channel)
class AdminChannel(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    inlines = [PostInline]

@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    inline = [PostInline]


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    fields = [('channel', 'title', 'tags'), ('text', 'image')]
    list_display = ('pubdate', 'channel', 'title', 'display_tag', 'rewritedate', 'display_image',)
    list_filter = ('pubdate', 'channel', 'title', 'rewritedate',)
    