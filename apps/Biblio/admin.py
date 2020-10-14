from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status')
    list_filter = ('status',  'publish')
    search_fields = ('title',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
