from django.urls import path
from . import views
from django.conf import settings

app_name = 'biblio'

urlpatterns = [
    path('public/catalog', views.CatalogView.as_view(), name='public_catalog'),
    path('mybooks', views.MyBooksView.as_view(), name='mybooks'),

    path('catalog/state_change', views.book_state_change, name='book_state_change'),
    path('book_create', views.BookCreateView.as_view(), name='book_create'),
    path('book_detail/<slug:slug>', views.book_detail, name='book_detail'),
]

if settings.DEBUG:
    urlpatterns += [path('populate', views.populate, name='populate')]