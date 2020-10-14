from django.urls import path
from . import views
from django.conf import settings

app_name = 'biblio'

urlpatterns = [
    path('catalog', views.catalog_list, name='catalog'),
    path('index', views.index, name='index'),
]