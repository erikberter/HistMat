from django.urls import path
from . import views
from django.conf import settings

app_name = 'biblio'

urlpatterns = [
    path('public/catalog/', views.CatalogView.as_view(), name='public_catalog'),
    path('mycatalog/', views.MyCatalogView.as_view(), name='mycatalog'),

    path('author/<slug:slug>/detail/', views.AuthorDetailView.as_view(), name='author_view'),
    
    path('book_create', views.BookCreateView.as_view(), name='book_create'),
    path('book_update/<slug:slug>/', views.BookUpdateView.as_view(), name='book_update'),
    path('book_delete/<slug:slug>/', views.BookDeleteView.as_view(), name='book_delete'),

    path('book_detail/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),

    path('book_detail/<slug:slug>/state_change', views.book_state_change, name='book_state_change'),
    path('book_detail/<slug:slug>/page_change', views.book_page_change, name='book_page_change'),
    path('book_detail/<slug:slug>/rate', views.book_rate, name='book_rate'),
]

if settings.DEBUG:
    urlpatterns += [path('populate', views.populate, name='populate')]