from django.forms import ModelForm, Form
from apps.Biblio.models import Book

class BookCreateForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'npages', 'cover' , 'book_file', 'visibility']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BookCreateForm, self).__init__(*args, **kwargs)

