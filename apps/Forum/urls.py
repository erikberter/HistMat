from django.urls import path
from django.conf import settings
from . import views

app_name = 'forum'

urlpatterns = [
    path("forum/", views.post_home , name='post_home'),
    path("forum/add_post", views.AddPostView.as_view(), name = 'add_post'),
    path("forum/post_detail/<int:pk>/", views.post_detail, name = 'post_detail'),
    path("forum/post_detail/<int:pk>/add_comment", views.AddPostView.as_view(), name = 'add_comment'),
    path("forum/post_detail/<int:pk>/upvote", views.postUpvote, name = 'post_upvote'),
    path("forum/post_detail/<int:pk>/downvote", views.postDownvote, name = 'post_downvote'),
]