from django.contrib import admin
from .models import *


class ApunteAdmin(admin.ModelAdmin):
    list_display = ('autor', 'nombre', 'paginas', 'likes')
    list_filter = ['created', 'updated']
    search_fields = ['autor', 'nombre' , 'paginas', 'likes']
    fieldsets = [
        ('Informacion Apunte', {'fields': ['nombre','documento', 'paginas', 'likes', 'thumbnail', 'categoria', 'tipo']}),
        ('Autor & Fechas', {'fields': ['autor', 'created', 'updated'], 'classes': ['collapse']}),
    ]

admin.site.register(Apunte, ApunteAdmin)