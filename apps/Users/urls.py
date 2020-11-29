from django.urls import path
from . import views
from django.conf import settings

from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view() , name='logout'),
    path('<int:pk>/user_detail/', views.user_detail, name='user_detail'),
    path('<int:pk>/user_config', views.UserUpdateView.as_view(), name='user_config'),
    path('achievements/', views.AchievementListView.as_view(), name='achievement_list'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/', views.UserListView.as_view(), name='user_list'),
]