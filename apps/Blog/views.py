from django.shortcuts import render

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import *

from braces.views import UserPassesTestMixin

# Create your views here.
class BlogCreateView(UserPassesTestMixin, CreateView):
    model = Blog
    fields = ['title', 'text', 'thumbnail']
    template_name = 'Blog/book_create.html'

    def test_func(self, user):
        is_valid = user == self.get_object().creator
        is_valid |= user.is_superuser
        is_valid |= user.is_content_editor
        return 
        

class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'text', 'thumbnail']
    template_name = 'Blog/book_update.html'

    def test_func(self, user):
        is_valid = user == self.get_object().creator
        is_valid |= user.is_superuser
        is_valid |= user.is_content_editor
        return is_valid


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'Blog/book_update.html'
    context_object_name = "blog"

class BlogListView(ListView):
    model = Blog
    template_name = 'Blog/book_update.html'
    paginate_by = 10
    context_object_name = "blogs"

class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = Blog
    context_object_name = "blog"
    template_name = 'Blog/blog_delete.html'
    login_url = '/login/'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self, user):
        is_valid = user == self.get_object().creator
        is_valid |= user.is_superuser
        return is_valid