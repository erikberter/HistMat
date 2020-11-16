from django.urls import path
from . import views
from django.conf import settings
from .views import post_home, post_detail, AddPostView, AddCommentView

from django.contrib.auth import views as auth_views

app_name = 'forum'

urlpatterns = [
    path('forum/', post_home , name='post_home'),
    path('post_detail/add_post', AddPostView.as_view(), name = 'add_post'),
    path('forum/post_detail/<int:pk>/', post_detail, name = 'post_detail'),
]