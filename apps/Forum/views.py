from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Post, Comment
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect

def post_home(request):
    posts = Post.objects.all()
    context = {'posts' : posts}
    return render(request, 'Forum/post_home.html', context)

def post_detail(request, pk, self):
    post = get_object_or_404(Post, pk=pk)
    post = self.get_object()

    return render(request, 'Forum/post_detail.html', {'post':post})

class AddPostView(CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = 'Forum/forms/add_post.html'

    success_url = reverse_lazy('post_home')

    fields = ["body", "image"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.success_url)

class AddCommentView(CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Comment
    template_name = 'Forum/forms/add_comment.html'

    success_url = reverse_lazy('post_detail')

    fields = ["body"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.success_url)

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