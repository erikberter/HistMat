from django.contrib import admin
from  .models import Achievement, Profile

# Register your models here.


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'country')


class UserRolAdmin(admin.ModelAdmin):
    list_display = ('user', 'level' 'xp')

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_cuantity', 'created_date')


admin.site.register(Achievement)
admin.site.register(Profile)