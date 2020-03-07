from django.contrib import admin
from .models import Blog, Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'added', 'updated', 'image']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body', 'added')

admin.site.register(Blog, BlogAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created', 'updated', 'body']

admin.site.register(Comment, CommentAdmin)
