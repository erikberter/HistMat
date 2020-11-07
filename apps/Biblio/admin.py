from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'visibility')
    list_filter = ('visibility',  'created')
    search_fields = ('title',)
    date_hierarchy = 'created'
    ordering = ('visibility', 'created')

admin.site.register(BookUserDetail)