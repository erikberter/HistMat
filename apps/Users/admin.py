from django.contrib import admin
from  .models import Achievement, Profile, Achievement_Progress,UserFollowing, ProfileStats

# Register your models here.


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_cuantity', 'created_date')


admin.site.register(Achievement)
admin.site.register(Profile)
admin.site.register(Achievement_Progress)
admin.site.register(UserFollowing)
admin.site.register(ProfileStats)