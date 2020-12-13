from django.shortcuts import render

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect

from .models import *

from braces.views import UserPassesTestMixin

# Create your views here.
class BlogCreateView(UserPassesTestMixin, CreateView):
    model = Blog
    fields = ['title', 'text', 'thumbnail']
    template_name = 'Blog/blog_create.html'

    def test_func(self, user):
        return user.is_superuser | user.is_content_editor
    
    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.autor = self.request.user
        blog.save()

        return HttpResponseRedirect(blog.get_absolute_url())

class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'text', 'thumbnail']
    template_name = 'Blog/blog_update.html'

    success_url = reverse_lazy("blog:blog_list")
    def test_func(self, user):
        return user.is_superuser |  user.is_content_editor

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'Blog/blog_detail.html'
    context_object_name = "blog"

class BlogListView(ListView):
    model = Blog
    template_name = 'Blog/blog_list.html'
    paginate_by = 10
    context_object_name = "blogs"

class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = Blog
    context_object_name = "blog"
    template_name = 'Blog/blog_delete.html'
    login_url = '/login/'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self, user):
        return ( user == self.get_object().creator ) | user.is_superuser