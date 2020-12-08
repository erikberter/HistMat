from django.urls import path
from . import views
from django.conf import settings

app_name = 'layout'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),
]