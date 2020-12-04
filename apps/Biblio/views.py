from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.db.models import Avg, Q

from django.http import  HttpResponseRedirect, Http404, JsonResponse

from django.shortcuts import render, get_object_or_404

from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from .models import Book, Author, BookUserDetail
from .forms import BookCreateForm
from .utils import *

import json

from slugify import slugify

from django.urls import reverse_lazy

from braces.views import UserPassesTestMixin

#########################################
#           Views Configuration         #
#########################################

CORRECT_JSON_DICT = {'status':'Success', 'msg': 'save successfully'}


#########################################
#                 Views                 #
#########################################


class CatalogView(ListView):
    model = Book
    context_object_name = 'books'

    template_name = 'Biblio/catalog.html'
    paginate_by = 20

    queryset = Book.public.all()


class MyCatalogView(LoginRequiredMixin, View):
    template_name = 'Biblio/mycatalog.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        if not data:
            raise Http404("Empty")

        data['shelf_title'] = data.get('book_state')
        data['book_state'] = slugify(data['shelf_title'].lower(), separator="_")

        # TODO simplificar con related_name
        books = Book.objects.filter(bookuserdetail__user=request.user).filter(bookuserdetail__book_state=data['book_state']).distinct()
        
        data['books'] = [book.assemble() for book in books]

        return JsonResponse(data)


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



class BookDetailView(DetailView):
    model = Book
    template_name = "Biblio/book_detail.html"
    context_object_name = "book"

    

    def get_queryset(self):
        books = Book.public.all()
        if self.request.user.is_authenticated:
            books = books | Book.objects.filter(bookuserdetail__user = self.request.user)

        return books.distinct()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['book_state'] = get_book_state(self.request.user, self.get_object())
        data['rating'] = self.get_object().users.aggregate(total = Avg('bookuserdetail__rating'))
        data['has_book'] =  is_book_in_user(self.request.user, self.get_object())
        if data['has_book']:
            data['act_page'] = get_user_act_page(self.request.user, self.get_object())
            data['own_rating'] = str(get_user_rating(self.request.user, self.get_object()))
        return data



class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'description', 'author', 'npages', 'book_file', 'cover', 'visibility', 'tags']
    template_name = 'Biblio/forms/book_update.html'

    def test_func(self, user):
        return user == self.get_object().creator

class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    context_object_name = "book"
    template_name = 'Biblio/forms/book_delete.html'
    login_url = '/login/'
    success_url = reverse_lazy('biblio:mycatalog')

    def test_func(self, user):
        return user == self.get_object().creator

class AuthorDetailView(DetailView):
    model = Author
    template_name = "Biblio/author_detail.html"
    context_object_name = "author"



@require_POST
def book_state_change(request, slug):
    book = Book.objects.get(slug=slug)
    if request.is_ajax():
        
        new_book_state = slugify(request.POST.get('book_state').lower(), separator="_")
        if not new_book_state:
            raise Http404("No valid book state")
        
        book_ud_c = BookUserDetail.objects.filter(
                book = book).filter(user = request.user).count()
        if(book_ud_c == 0):
            book_ud = BookUserDetail.objects.create(book=book, user = request.user)
        else:
            book_ud = BookUserDetail.objects.filter(
                book = book).filter(user = request.user).first()
        
        book_ud.book_state = new_book_state
        book_ud.save()

        return JsonResponse(CORRECT_JSON_DICT)
        



@require_POST
def book_page_change(request, slug):
    if request.is_ajax():
        new_act_page = request.POST.get('act_page')
        if not new_act_page:
            raise Http404("Invalid Actual Page")

        book = Book.objects.get(slug=slug)
        
        book_ud = get_object_or_404(BookUserDetail,
                book=book,
                user = request.user
            )

        book_ud.act_page = new_act_page
        book_ud.save()
        return JsonResponse(CORRECT_JSON_DICT)


@require_POST
def book_rate(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if "rating_v" in request.POST:
        budetail = BookUserDetail.objects.filter(book=book).distinct().get(user = request.user)
        budetail.rating = int(request.POST.get("rating_v"))
        budetail.save()
    return HttpResponseRedirect(book.get_absolute_url())

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
        book_state = random.choice(book_state_l)
        book_du = BookUserDetail.objects.create(book=book, user=Profile.objects.order_by('?')[0], book_state=book_state)
        
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