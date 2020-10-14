from django.shortcuts import render
from .models import Book


# Create your views here.
def catalog_list(request):
    libros = Book.objects.all()
    return render(request, 'Biblio/catalog.html', {"libros" : libros})


def index(request):
    context = {
        'posts': Book.objects.all()
        if request.user.is_authenticated else []
    }

    return render(request, 'blog/index.html', context)