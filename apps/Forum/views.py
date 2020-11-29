from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
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
    template_name = 'Forum/forms/add_post.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save()
        post.user = self.request.user
        post.save()
        return HttpResponseRedirect(post.get_absolute_url())

    success_url = reverse_lazy('post_home')

class AddCommentView(CreateView):
    model = Comment
    template_name = 'Forum/forms/add_comment.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save()
        post.user = self.request.user
        post.save()
        return HttpResponseRedirect(post.get_absolute_url())

    success_url = reverse_lazy('post_detail')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def postUpvote(request, pk):
    if request.method == "POST":
        if request.is_ajax():
            if "like" in request.POST:
                post = Post.objects.get(pk=pk)
                post.likes += 1
                post.save()
    return JsonResponse({'status':'Success', 'msg': 'save successfully'})

@csrf_exempt
def postDownvote(request, pk):
    if request.method == "POST":
        if request.is_ajax():
            if "like" in request.POST:
                post = Post.objects.get(pk=pk)
                post.likes -= 1
                post.save()
    return JsonResponse({'status':'Success', 'msg': 'save successfully'})

@csrf_exempt
def commentUpvote(request, pk):
    if request.method == "POST":
        if request.is_ajax():
            if "like" in request.POST:
                comment = Comment.objects.get(pk=pk)
                comment.likes += 1
                comment.save()
    return JsonResponse({'status':'Success', 'msg': 'save successfully'})

@csrf_exempt
def commentDownvote(request, pk):
    if request.method == "POST":
        if request.is_ajax():
            if "like" in request.POST:
                comment = Comment.objects.get(pk=pk)
                comment.likes -= 1
                comment.save()
    return JsonResponse({'status':'Success', 'msg': 'save successfully'})