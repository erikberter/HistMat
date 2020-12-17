from django.urls import path
from . import views

from django.views.decorators.cache import cache_page

app_name = 'forum'

urlpatterns = [
    path("", views.PostHomeView.as_view() , name='post_home'),
    path("add_post", views.AddPostView.as_view(), name = 'add_post'),
    path("post_detail/<int:pk>/", cache_page(60 * 60)(views.PostDetailView.as_view()), name = 'post_detail'),
    path("post_detail/<int:pk>/add_comment", views.add_comment, name = 'add_comment'),
    path("post_detail/<int:pk>/upvote", views.postUpvote, name = 'post_upvote'),
]