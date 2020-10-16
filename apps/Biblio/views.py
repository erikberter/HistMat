from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound

from django.db.models import Q


from .models import Book, Author
from .forms import BookCreateForm

# Create your views here.
def catalog(request):
    
    context = {}

    if request.user.is_authenticated:
        context['books_user'] = Book.objects.filter(publications=request.user)
    else:
        context['books_all'] =  Book.objects.filter(status="public")

    return render(request, 'Biblio/catalog.html', context)


def book_detail(request, slug):
    if not request.user.is_authenticated:
        book = Book.objects.filter(slug=slug, status="public").first()
    else:
        book = Book.objects.filter(slug=slug).filter(Q(publications=request.user) | Q(status="public")).first()
    if book == None:
        return HttpResponseNotFound("Book not found")  
    context = {
        'book' : book,
    }
    return render(request, 'Biblio/book_detail.html', context)


def create_book(request):
    if request.method == "POST":
        bookform = BookCreateForm(request.POST)
        if bookform.is_valid():
            bookform.save()
        else:
            # TODO Add custom template for error
            pass
    bookform = BookCreateForm()
    return render(request, 'Biblio/forms/book_create.html', {'bookform': bookform})


#### DELETE  IN PRODUCTION 

import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def populate(request):
    context = {}
    if request.method == 'POST':
        n_author    = request.POST['n_author'] 
        n_book      = request.POST['n_book']

        same_user   = request.POST['same_user']

        for i in range(int(n_author)):
            Author.objects.create(name= get_random_string(15))
        for i in range(int(n_book)):
            book = Book()
            book.title = get_random_string(15)
            book.author = Author.objects.order_by('?')[0]
            
            book.npages = random.randint(10,500)

            book.save()
            if same_user == "Yes":
                book.publications.add(request.user)
            else:
                book.publications.add(User.objects.order_by('?')[0])
            book.save()
        return HttpResponseRedirect(request.path_info)
    return render(request,'biblio/populate.html', context)