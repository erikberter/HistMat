from django.urls import path
from . import views

app_name = 'apuntes'

urlpatterns = [

path('apuntes/', views.ApuntesListView.as_view(), name = 'apuntes'),
path('add_apuntes/', views.ApunteCreateView.as_view(), name = 'add_apuntes'),
path('apuntes_detail/<int:pk>/', views.ApuntesDetailView.as_view(), name = 'apuntes_detail'),
path('apuntes_remove/<int:pk>/remove/', views.apuntes_remove, name='apuntes_remove'),
path('apuntes_update/<int:pk>/', views.ApunteUpdateView.as_view(), name = 'apuntes_update'),
]