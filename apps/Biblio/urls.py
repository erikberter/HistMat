from django.urls import path
from . import views
from django.conf import settings

app_name = 'biblio'

urlpatterns = [
    path('catalog', views.catalog, name='catalog'),
    path('populate', views.populate, name='populate'),
    path('book_detail/<slug:slug>', views.book_detail, name='book_detail'),
]