from django.contrib import admin

# Register your models here.
from .models import Channel, Tag, Post, Image


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
    fields = [('title'), ('channel', 'img'), ('text',  'tags')]
    list_display = ('title', 'channel', 'display_tag', 'pubdate', 'display_image', 'display_img_path', 'rewritedate',)
    list_filter = ('pubdate', 'channel', 'title', 'rewritedate',)


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ('post', 'created_time', 'id',)
    list_filter = ('created_time',)