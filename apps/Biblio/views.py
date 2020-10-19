from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404

from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt

from .models import Book, Author, BookUserDetail
from .forms import BookCreateForm

# TODO Try to delete the decorator
@csrf_exempt
def catalog(request):
    
    context = {}

    if request.is_ajax():
        if 'book_self' in request.POST:
            book_self = request.POST.get('book_self')
            books = None
            if book_self == 'public':
                books = Book.objects.filter(visibility='public')
            elif request.user.is_authenticated:
                books = request.user.book_set.filter(bookuserdetail__book_state=book_self)
            else:
                raise Http404("Anonymous User trying to access non valid data")  
            
            if 'search_book' in request.POST:
                if request.POST.get('search_book'):
                    books = books.filter(title__contains = request.POST.get('search_book'))
            
            context['books'] = books
            return render(request, 'Biblio/_books.html', context)
        else:
            raise Http404("Book Self not found")  

    return render(request, 'Biblio/catalog.html', context)


def book_detail(request, slug):
    if not request.user.is_authenticated:
        book = get_object_or_404(Book, Q(slug=slug) & Q(visibility="public"))
    else:
        book = get_object_or_404(Book,
            Q(slug=slug) & ( Q(bookuserdetail__user = request.user) |  Q(visibility="public") )
        )

    context = {}
    context['book'] = book

    return render(request, 'Biblio/book_detail.html', context)


def create_book(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound("Can't create withour account")  

    if request.method == "POST":
        bookform = BookCreateForm(request.POST, request.FILES)
        if bookform.is_valid():
            book = bookform.save()
            book_du = BookUserDetail.objects.create(book=book, user=request.user)
            book_du.save()
            book.save()
            return HttpResponseRedirect(book.get_absolute_url())
        else:
            # TODO Add custom template for error
            print("NOSE PUEDE")
            pass
    bookform = BookCreateForm()
    return render(request, 'Biblio/forms/book_create.html', {'bookform': bookform})


#### DELETE  IN PRODUCTION 

import random
import string
from django.core.files import File  # you need this somewhere
import urllib.request
import os

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def populate(request):
    context = {}
    book_state_l = ['reading','want_to_read','read']
    book_status = ['private','public']
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
            book.visibility = random.choice(book_status)
            book.npages = random.randint(10,500)

            book.save()
            result = urllib.request.urlretrieve("https://d1csarkz8obe9u.cloudfront.net/posterpreviews/action-thriller-book-cover-design-template-3675ae3e3ac7ee095fc793ab61b812cc_screen.jpg?ts=1588152105")
            book.cover.save(os.path.basename("Algo"), File(open(result[0], 'rb')))
            book_du = BookUserDetail.objects.create(book=book, user=User.objects.order_by('?')[0], book_state=random.choice(book_state_l))
            book_du.save()
            book.save()
        return HttpResponseRedirect("catalog")
    return render(request,'biblio/populate.html', context)