from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Book, Author, BookUserDetail
from .forms import BookCreateForm

BOOK_PER_PAGE = 13




def __get_book_by_paginator(books, page):
    paginator = Paginator(books, BOOK_PER_PAGE) 

    if page > paginator.num_pages:
        return books, -1

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return books, 1

def __get_public_book_list(request):
    return {'books': Book.objects.filter(visibility='public')}

def __get_public_book_list_page(request):
    context = __get_public_book_list(request)

    
    page = 1
    if 'page' in request.GET:
        page = int(request.GET.get('page'))

    books, validator = __get_book_by_paginator(context['books'], page)

    context['books'] = books
    context['validator'] = validator
    return context

# TODO Try to delete the decorator
@csrf_exempt
def catalog(request):
    context  = __get_public_book_list_page(request)

    if request.is_ajax():
        if context['validator'] == -1:
            raise Http404
        return render(request,"Biblio/_books_no_ul.html",context)

    return render(request, 'Biblio/catalog.html', context)


@login_required
@csrf_exempt
def mybooks(request):
    
    context = {}
    if request.is_ajax():
        if 'book_state' in request.POST:
            context['book_state'] = request.POST.get('book_state')
            
            books = request.user.book_set.filter(bookuserdetail__book_state=context['book_state'])
            
            if 'search_book' in request.POST:
                if request.POST.get('search_book'):
                    books = books.filter(title__contains = request.POST.get('search_book'))
            
            context['books'] = books
            return render(request, 'Biblio/_books.html', context)
        else:
            raise Http404("Book Self not found")  

    return render(request, 'Biblio/mybooks.html', context)


@csrf_exempt
def book_state_change(request):
    context={}
    if request.is_ajax() and request.method == 'POST':
        if 'book_pk' in request.POST and 'book_state' in request.POST:

            book_pk = request.POST.get('book_pk')
            book = Book.objects.get(pk=book_pk)

            book_ud_c = BookUserDetail.objects.filter(
                 Q(book=book) & Q(user = request.user) 
            ).count()

            if book_ud_c == 0:
                book_ud = BookUserDetail()
                book_ud.user = request.user
                book_ud.book = book
            else:
                book_ud = BookUserDetail.objects.filter(
                 Q(book=book) & Q(user = request.user) 
                ).first()
            
            book_ud.book_state = request.POST.get('book_state')
            book_ud.save()

            return JsonResponse({'status':'Success', 'msg': 'save successfully'})
        else:
            raise Http404("State or Pk not found")



def book_detail(request, slug):
    context = {}
    if not request.user.is_authenticated:
        context['book'] = get_object_or_404(Book, Q(slug=slug) & Q(visibility="public"))
    else:
        try:
            context['book'] = Book.objects.get(
            Q(slug=slug) & ( Q(bookuserdetail__user = request.user) |  Q(visibility="public") )
            )
        except:
            raise Http404

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
        return HttpResponseRedirect("mybooks")
    return render(request,'biblio/populate.html', context)