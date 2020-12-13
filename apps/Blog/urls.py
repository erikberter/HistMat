from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    
    path('blog_create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog_list/',  views.BlogListView.as_view(), name='blog_list'),
    path('blog_update/<slug:slug>/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<slug:slug>/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog_detail/<slug:slug>/',  views.BlogDetailView.as_view(), name='blog_detail'),

]