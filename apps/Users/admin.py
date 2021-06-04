from django.contrib import admin
from  .models import  Profile,  ProfileStats
from apps.Biblio.models import BookUserDetail
from apps.Forum.models import Post, Comment


class StatsInLine(admin.TabularInline):
    model = ProfileStats
    extra = 1

class BookInLine(admin.TabularInline):
    model = BookUserDetail
    extra = 1

class PostInLine(admin.TabularInline):
    model = Post
    extra = 1

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['date_joined', 'last_login', 'is_superuser', 'is_content_editor', 'is_active']
    list_display = ('username', 'first_name' , 'last_name', 'email', 'is_active')
    search_fields = ['username', 'first_name' , 'last_name', 'email', 'country']
    fieldsets = [
        ('Informacion Personal', {'fields': ['username','password', 'first_name', 'last_name', 'email', 'profile_image', 'study_center', 'country', 'city', 'born_date']}),
        ('Pagina Web & Redes Sociales', {'fields': ['website', 'github', 'instagram', 'twitter', 'facebook'], 'classes': ['collapse']}),
        ('Rol & Amigos', {'fields': ['level', 'xp', 'kind_of_user', 'following'], 'classes': ['collapse']}),
        ('Informacion Tecnica', {'fields': ['last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff','is_content_editor', 'user_permissions', 'groups'], 'classes': ['collapse']}),
    ]
    inlines = [ StatsInLine, BookInLine,  PostInLine, CommentInLine]


class ProfileStatsAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ('user','like_counter','view_counter','book_upload_counter','book_readed_counter','following_counter')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileStats, ProfileStatsAdmin)