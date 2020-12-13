from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect

from .models import Post, Comment
from .forms import PostForm, CommentForm
from .utils import *

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator


from apps.UserMechanics.models import ActionPostComment, ActionPostAdd, ActionPostLike

from braces.views import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class PostHomeView(ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'Forum/post_home.html'
    paginate_by = 10

def add_comment(request, pk):
    if not request.user.is_authenticated:
        return redirect('forum:post_detail', pk=pk)

    form = CommentForm(request.POST)
    if form.is_valid():
        post = get_object_or_404(Post, pk=pk)
        comment = form.save(commit=False)
        
        if 'parent_id' in request.POST:
            if request.POST['parent_id']:
                parent_id = int(request.POST['parent_id'])
                if Comment.objects.filter(pk=parent_id).exists():
                    comment.parent = Comment.objects.get(pk=parent_id)
        
        comment.user = request.user
        comment.post = post
        comment.save()

        request.user.add_exp(2)
        ActionPostComment.objects.create(autor = request.user, post = post, comment=comment)

    return redirect('forum:post_detail', pk=pk)

class PostDetailView(DetailView):
    model = Post
    template_name = 'Forum/post_detail.html'
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = CommentForm

        _list = Comment.objects.filter(post=self.kwargs.get('pk'))
        paginator = Paginator(_list, 20) 
        page = self.request.GET.get('page')
        data['comments'] = paginator.get_page(page)

        return data

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'Forum/forms/add_post.html'
    form_class = PostForm
    success_url = reverse_lazy('forum:post_home')

    def form_valid(self, form):
        post = form.save()
        post.user = self.request.user
        post.save()

        self.request.user.add_exp(5)
        ActionPostAdd.objects.create(autor = self.request.user, post = post)

        return HttpResponseRedirect(post.get_absolute_url())

def postUpvote(request, pk):
    if not request.user.is_authenticated:
        raise Http404("Anonymous user liked post")

    if request.method == "POST":
        if request.is_ajax():
            post = Post.objects.get(pk=pk)

            if is_post_liked(post, request.user):
                post.likes -= 1
                ActionPostLike.objects.filter(autor=request.user).filter(post = post).delete()
            else:
                post.likes += 1
                request.user.add_exp(1)
                ActionPostLike.objects.create(autor = request.user, post = post)

            post.save()

    return JsonResponse({'status':'Success', 'msg': 'save successfully'})