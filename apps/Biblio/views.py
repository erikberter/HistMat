from django.shortcuts import render
from .models import Book


# Create your views here.
def catalog_list(request):
    post_whiwho = Book.objects.filter(publications=request.user)
    context = {
        'posts_all': Book.objects.all()
        if request.user.is_authenticated else [], 
        'post_whiwho' : post_whiwho
    }
    return render(request, 'Biblio/catalog.html', context)


def index(request):
    post_whiwho = Book.objects.filter(publications=request.user)
    context = {
        'posts_all': Book.objects.all()
        if request.user.is_authenticated else [], 
        'post_whiwho' : post_whiwho
    }

    return render(request, 'blog/index.html', context)