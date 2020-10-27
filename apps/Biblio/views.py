from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import  HttpResponseRedirect, Http404, JsonResponse
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Book, Author, BookUserDetail
from .forms import BookCreateForm

import json

BOOK_PER_PAGE = 13

class CatalogView(ListView):
    paginate_by = 20
    model = Book
    context_object_name = 'books'
    template_name = 'Biblio/catalog.html'

    def get_queryset(self):
          return Book.public.all()



class MyBooksView(LoginRequiredMixin, View):
    template_name = 'Biblio/mybooks.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            
            context ={}
            if 'book_state' in request.POST:
                if not request.POST.get('book_state'):
                    raise Http404("Empty")

                context['book_state'] = request.POST.get('book_state')
                context['shelf_sortable'] = "Sortable"+context['book_state']
                context['shelf_title'] = context['book_state']
                context['div_id'] = "Container" + context['book_state']
                context['books'] = request.user.book_set.filter(bookuserdetail__book_state=context['book_state'])

                if 'search_book' in request.POST:
                    if request.POST.get('search_book'):
                        context[book_state] = context[book_state].filter(title__contains = request.POST.get('search_book'))
        
                return render(request, 'Biblio/_book_shelf_list.html', context)
            else:
                raise Http404("Book Self not found") 

    def get(self, request):
        return render(request, 'Biblio/mybooks.html')

@require_POST
def book_state_change(request):
    context={}
    if request.is_ajax():
        if 'book_pk' in request.POST and 'book_state' in request.POST:
            book_pk = int(request.POST.get('book_pk'))
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
        context['book'] = get_object_or_404(Book,
            Q(slug=slug) & ( Q(bookuserdetail__user = request.user) |  Q(visibility="public") )
        )

    return render(request, 'Biblio/book_detail.html', context)

class BookCreateView(LoginRequiredMixin, CreateView):
    template_name = 'Biblio/forms/book_create.html'
    form_class = BookCreateForm

    def form_valid(self, form):
        book = form.save()
        book_du = BookUserDetail.objects.create(book=book, user=self.request.user)
        book_du.save()
        book.save()
        return HttpResponseRedirect(book.get_absolute_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BookCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

from config.settings.settings import DEBUG

if DEBUG:
    import random
    from .utils import get_random_string
    from django.core.files import File  # you need this somewhere
    import urllib.request
    import os


    def add_random_book():
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
            return HttpResponseRedirect("mybooks")
        return render(request,'biblio/populate.html', context)