from django.urls import path
from . import views
from django.conf import settings

from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view() , name='logout'),
]