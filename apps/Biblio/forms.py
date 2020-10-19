from django.forms import ModelForm
from apps.Biblio.models import Book

class BookCreateForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'npages', 'cover' , 'book_file', 'visibility']