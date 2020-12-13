from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view() , name='logout'),
    path('<int:pk>/user_detail/', views.user_detail, name='user_detail'),
    path('<int:pk>/user_detail/seguir/', views.seguir, name='seguir'),
    path('<int:pk>/user_config', views.UserUpdateView.as_view(), name='user_config'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/search/', views.search_view, name='user_search'),
]