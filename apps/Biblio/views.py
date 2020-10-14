from django.shortcuts import render
from .models import Book


# Create your views here.
def catalog_list(request):
    libros = Book.objects.all()
    return render(request, 'Biblio/catalog.html', {"libros" : libros})