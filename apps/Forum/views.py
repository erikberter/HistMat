from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect

from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator


class PostHomeView(ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'Forum/post_home.html'
    paginate_by = 10

def add_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        post = get_object_or_404(Post, pk=pk)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        user_mechs.add_exp(request.user, 2)
    return redirect('forum:post_detail', pk=pk)

class PostDetailView(DetailView):
    model = Post
    template_name = 'Forum/post_detail.html'
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = CommentForm

        _list = Comment.objects.filter(post=self.kwargs.get('pk'))
        paginator = Paginator(_list, 2) 
        page = self.request.GET.get('page')
        data['comments'] = paginator.get_page(page)

        return data

class AddPostView(CreateView):
    model = Post
    template_name = 'Forum/forms/add_post.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save()
        post.user = self.request.user
        post.save()
        user_mechs.add_exp(request.user, 5)
        return HttpResponseRedirect(post.get_absolute_url())

    success_url = reverse_lazy('forum:post_home')

from django.views.decorators.csrf import csrf_exempt

def postUpvote(request, pk):
    if request.method == "POST":
        if request.is_ajax():
            post = Post.objects.get(pk=pk)
            post.likes += 1
            post.save()
            user_mechs.add_exp(request.user, 1)
    return JsonResponse({'status':'Success', 'msg': 'save successfully'})