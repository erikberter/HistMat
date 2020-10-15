from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .models import Book, Author


# Create your views here.
def catalog(request):
    
    context = {}

    if request.user.is_authenticated:
        context['books_user'] = Book.objects.filter(publications=request.user)
    else:
        context['books_all'] =  Book.objects.filter(status="public")

    return render(request, 'Biblio/catalog.html', context)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    context = {
        'book' : book,
    }
    return render(request, 'Biblio/book_detail.html', context)


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