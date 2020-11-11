from django.urls import path
from . import views

app_name = 'apuntes'

urlpatterns = [

path('apuntes/', views.apuntes, name = 'apuntes'),

]