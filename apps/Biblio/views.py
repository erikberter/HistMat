from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Avg

from django.http import  HttpResponseRedirect, Http404, JsonResponse

from django.shortcuts import render, get_object_or_404



from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST


from .models import Book, Author, BookUserDetail
from .forms import BookCreateForm
from .utils import *

import json

from slugify import slugify

from django.urls import reverse_lazy

from braces.views import UserPassesTestMixin

from apps.UserMechanics.models import *

from sorl.thumbnail import get_thumbnail
from pinax.badges.registry import badges

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
        if not data:
            raise Http404("Empty")

        data['shelf_title'] = data.get('book_state')
        data['book_state'] = slugify(data['shelf_title'].lower(), separator="_")

        books = request.user.added_books.filter(books_details__book_state=data['book_state'])
        
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
        book.save(thumbnail=True)
    
        
        self.request.user.add_exp(10)
        badges.possibly_award_badge("book_added", user=self.request.user)
        ActionBookAdd.objects.create(autor = self.request.user, book = book, 
            visibility=form.instance.visibility)

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
            books = books | self.request.user.added_books.all()

        return books.distinct()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['rating'] = self.get_object().users.aggregate(total = Avg('books_details__rating'))
        data['has_book'] = False
        
        if self.request.user.is_authenticated:
            book_details = self.get_object().books_details.filter(user=self.request.user)

            data['has_book'] =  book_details.exists()
            data['book_state'] = 'None'
            if data['has_book']:
                data.update(book_details.first().assemble())

        return data



class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'description', 'author', 'npages', 'book_file', 'cover', 'visibility', 'tags']
    template_name = 'Biblio/forms/book_update.html'

    def form_valid(self, form):
        super(BookUpdateView, self).form_valid(form)

        book = self.get_object()
        book.save(thumbnail=True)

        ActionBookAdd.objects.filter(
            autor = request.user
        ).filter(
            book=book
        ).update(
            visibility = form.instance.visibility
        )

        return HttpResponseRedirect(book.get_absolute_url())

    def test_func(self, user):
        return ( user == self.get_object().creator ) | user.is_superuser | user.is_content_editor

class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    context_object_name = "book"
    template_name = 'Biblio/forms/book_delete.html'
    login_url = '/login/'
    success_url = reverse_lazy('biblio:mycatalog')

    def test_func(self, user):
        return ( user == self.get_object().creator ) | user.is_superuser

class AuthorDetailView(DetailView):
    model = Author
    template_name = "Biblio/author_detail.html"
    context_object_name = "author"



@require_POST
def book_state_change(request, slug):
    print("--------------------------")
    book = Book.objects.get(slug=slug)
    if request.is_ajax():
        new_book_state = slugify(request.POST.get('book_state').lower(), separator="_")
        if not new_book_state:
            raise Http404("No valid book state")
        if not request.user.books_details.filter(book = book).exists():
            book_ud = BookUserDetail.objects.create(book=book, user = request.user)
        else:
            book_ud = request.user.books_details.get(book = book)
        
        book_ud.book_state = new_book_state
        book_ud.save()

        request.user.add_exp(1)
        ActionBookState.objects.create(autor = request.user, book = book, status=new_book_state)

        return JsonResponse(CORRECT_JSON_DICT)
        
@require_POST
def book_page_change(request, slug):
    if request.is_ajax():
        new_act_page = request.POST.get('act_page')
        if not new_act_page:
            raise Http404("Invalid Actual Page")

        book = Book.objects.get(slug=slug)
        
        budetail = get_object_or_404(BookUserDetail, book=book, user = request.user)
        budetail.act_page = new_act_page
        budetail.save(update_fields=['act_page'])
        request.user.add_exp(1)
        ActionBookPageChange.objects.create(autor = request.user, book = book, page=new_act_page)

        return JsonResponse(CORRECT_JSON_DICT)


@require_POST
def book_rate(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if "rating_v" in request.POST:
        rating = int(request.POST.get("rating_v"))
        budetail = request.user.books_details.get(book = book)
        budetail.rating = rating
        budetail.save(update_fields=['rating'])
        
        request.user.add_exp(2)
        ActionBookRate.objects.create(autor = request.user, book = book, valoracion=budetail.rating)

    return HttpResponseRedirect(book.get_absolute_url())
