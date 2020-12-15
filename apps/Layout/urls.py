from django.urls import path
from . import views

app_name = 'layout'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]