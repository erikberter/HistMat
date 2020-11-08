from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import  HttpResponseRedirect, Http404, JsonResponse
from django.db.models import Avg, Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Book, Author, BookUserDetail
from .forms import BookCreateForm

import json

from slugify import slugify

BOOK_PER_PAGE = 13




class CatalogView(ListView):
    paginate_by = 20
    model = Book
    context_object_name = 'books'
    template_name = 'Biblio/catalog.html'

    def get_queryset(self):
          return Book.public.all()



class MyCatalogView(LoginRequiredMixin, View):
    template_name = 'Biblio/mycatalog.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            
            context ={}
            if 'book_state' in request.POST:
                if not request.POST.get('book_state'):
                    raise Http404("Empty")
                
                context['shelf_title'] = request.POST.get('book_state')
                context['book_state'] = slugify(context['shelf_title'], separator="_")
                context['books'] = Book.objects.filter(bookuserdetail__user=request.user).filter(bookuserdetail__book_state=context['book_state'])
                
                context['book_state'] = slugify(context['shelf_title'])
                if 'search_book' in request.POST:
                    if request.POST.get('search_book'):
                        context[book_state] = context[book_state].filter(title__contains = request.POST.get('search_book'))
                if 'book_order' in request.POST:
                    order = request.POST.get('book_order')
                    if order=="order-last-added":
                        context['books'] = context['books'].order_by("bookuserdetail__updated")
                        print("-----2------")
                        print(context['books'])
                    elif order == "order-first-added":
                        context['books'] = context['books'].order_by("-bookuserdetail__updated")
                        print("-----1------")
                        print(context['books'])

                return render(request, 'Biblio/_book_shelf_list.html', context)
            else:
                raise Http404("Book Self not found") 

    def get(self, request):
        return render(request, 'Biblio/mycatalog.html')

@require_POST
def book_state_change(request, slug):
    context={}
    if request.is_ajax():
        book = Book.objects.get(slug=slug)
        
        book_ud_c = BookUserDetail.objects.filter(book=book).filter(user = request.user).count()

        if book_ud_c == 0:
            book_ud = BookUserDetail.objects.create(user = request.user, book=book)
        else:
            book_ud = BookUserDetail.objects.filter(book=book).get(user = request.user) 
            
        book_ud.book_state = request.POST.get('book_state')
        book_ud.save()
        return JsonResponse({'status':'Success', 'msg': 'save successfully'})
        
@require_POST
def book_page_change(request, slug):
    context={}
    if request.is_ajax():
        print("hola")
        book = Book.objects.get(slug=slug)
        
        book_ud_c = BookUserDetail.objects.filter(book=book).filter(user = request.user).count()

        if book_ud_c == 0:
            raise Http404("Book not found")
        else:
            book_ud = BookUserDetail.objects.filter(book=book).get(user = request.user) 
            
        book_ud.act_page = request.POST.get('act_page')
        book_ud.save()
        return JsonResponse({'status':'Success', 'msg': 'save successfully'})


def book_detail(request, slug):
    context = {}

    if not request.user.is_authenticated:
        context['book'] = get_object_or_404(Book, slug=slug, visibility="public")
    else:
        context['book'] = Book.objects.filter(slug=slug).filter(
            Q(bookuserdetail__user = request.user) | Q(visibility="public")
        ).distinct().first()

    if context['book'] == None:
        raise Http404("Book not found")

    if request.method == 'POST':
        if "book_state" in request.POST:
            
            book_ud_c = BookUserDetail.objects.filter(book=context['book']).filter(user = request.user).distinct().count()
            
            if book_ud_c == 0:
                book_ud = BookUserDetail.objects.create(user = request.user, book=context['book'])
            else:
                book_ud = BookUserDetail.objects.filter(book=context['book']).distinct().get(user = request.user)
                
            book_state_t = slugify(request.POST.get('book_state'))

            if book_state_t == "none":
                book_ud.delete()
            else:
                book_ud.book_state = slugify(request.POST.get('book_state'), separator='_')
                book_ud.save()
                
        if "rating_v" in request.POST:
            budetail = BookUserDetail.objects.filter(book=context['book']).distinct().get(user = request.user)
            budetail.rating = int(request.POST.get("rating_v"))
            budetail.save()

    context['rating'] = context['book'].users.aggregate(total = Avg('bookuserdetail__rating'))
    return render(request, 'Biblio/book_detail.html', context)

class BookCreateView(LoginRequiredMixin, CreateView):
    template_name = 'Biblio/forms/book_create.html'
    form_class = BookCreateForm

    def form_valid(self, form):
        book = form.save()
        book.creator = self.request.user
        book_du = BookUserDetail.objects.create(book=book, user=self.request.user)
        book_du.save()
        book.save()
        return HttpResponseRedirect(book.get_absolute_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BookCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs



class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'description', 'author', 'npages', 'book_file', 'cover', 'visibility']
    template_name = 'Biblio/forms/book_update.html'





from config.settings.settings import DEBUG

if DEBUG:
    import random
    from .utils import get_random_string
    from django.core.files import File  # you need this somewhere
    import urllib.request
    import os
    from apps.Users.models import Profile

    def add_random_book():
        book_state_l = ['reading','want_to_read','read']
        book_status = ['private','public']
        book = Book()
        book.title = get_random_string(15)
        book.author = Author.objects.order_by('?')[0]
        book.visibility = random.choice(book_status)
        book.npages = random.randint(10,500)
        book.save()
        result = urllib.request.urlretrieve("https://d1csarkz8obe9u.cloudfront.net/posterpreviews/action-thriller-book-cover-design-template-3675ae3e3ac7ee095fc793ab61b812cc_screen.jpg?ts=1588152105")
        book.cover.save(os.path.basename("Algo"), File(open(result[0], 'rb')))
        book_du = BookUserDetail.objects.create(book=book, user=Profile.objects.order_by('?')[0], book_state=random.choice(book_state_l))
        book_du.save()
        book.save()

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
                add_random_book()
            return HttpResponseRedirect("mycatalog")
        return render(request,'biblio/populate.html', context)