from django.contrib import admin
from .models import Post, Comment

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = ('user', 'body' , 'date', 'likes')
    search_fields = ['user', 'body' , 'date', 'likes']
    inlines = [CommentInLine]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post' , 'body', 'likes')
    search_fields = ['user', 'post' , 'body', 'likes']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
