from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Post, Comment
from .forms import PostForm


def post_home(request):
    posts = Post.objects.all()
    context = {'posts' : posts}
    return render(request, 'Forum/post_home.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'Forum/post_detail.html', {'post':post})

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'Forum/add_post.html'
    def form_valid(self, form):
        form.instance.post = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('post_home')

class AddCommentView(CreateView):
    model = Comment
    template_name = ''
    fields = ['body']
    success_url = reverse_lazy('post_home')