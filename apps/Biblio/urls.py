from django.urls import path
from . import views
from django.conf import settings

app_name = 'biblio'

urlpatterns = [
    path('catalog/public', views.public_catalog, name='public_catalog'),
    path('catalog', views.catalog, name='catalog'),

    path('catalog/state_change', views.book_state_change, name='book_state_change'),
    path('book_create', views.create_book, name='book_create'),
    path('book_detail/<slug:slug>', views.book_detail, name='book_detail'),

    # DELETE ON PRODUCTION
    path('populate', views.populate, name='populate'),
]