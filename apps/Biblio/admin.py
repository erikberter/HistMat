from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'visibility')
    list_filter = ('visibility',  'publish')
    search_fields = ('title',)
    date_hierarchy = 'publish'
    ordering = ('visibility', 'publish')
