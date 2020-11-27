from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Post, Comment
from django.db.models import Q

def post_home(request):
    posts = Post.objects.all()
    context = {'posts' : posts}
    return render(request, 'Forum/post_home.html', context)

def post_detail(request, pk, self):
    post = get_object_or_404(Post, pk=pk)
    post = self.get_object()

    return render(request, 'Forum/post_detail.html', {'post':post})

class AddPostView(CreateView):
    model = Post
    template_name = 'Forum/forms/add_post.html'
    success_url = reverse_lazy('post_home')
    fields = ['body', 'image']

class AddCommentView(CreateView):
    model = Comment
    template_name = 'Forum/post_detail.html'
    fields = ['body']
    success_url = reverse_lazy('post_home')