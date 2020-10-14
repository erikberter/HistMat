from django.urls import path
from . import views


app_name = 'biblio'

urlpatterns = [
    path('catalog', views.catalog_list, name='cataog'),
]