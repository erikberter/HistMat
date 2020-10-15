from django.urls import path
from . import views
from django.conf import settings

app_name = 'layout'

urlpatterns = [
    path('', views.index, name='index'),
]