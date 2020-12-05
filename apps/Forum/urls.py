from django.urls import path
from django.conf import settings
from . import views

app_name = 'forum'

urlpatterns = [
    path("forum/", views.PostHomeView.as_view() , name='post_home'),
    path("forum/add_post", views.AddPostView.as_view(), name = 'add_post'),
    path("forum/post_detail/<int:pk>/", views.PostDetailView.as_view(), name = 'post_detail'),
    path("forum/post_detail/<int:pk>/add_comment", views.add_comment, name = 'add_comment'),
    path("forum/post_detail/<int:pk>/upvote", views.postUpvote, name = 'post_upvote'),
]