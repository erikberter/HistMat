from django.urls import path
from . import views
from django.conf import settings

app_name = 'forum'

urlpatterns = [
    path("forum/", views.post_home , name='post_home'),
    path("forum/add_post", views.AddPostView.as_view(), name = 'add_post'),
    path("forum/post_detail/<int:pk>/", views.post_detail, name = 'post_detail'),
]