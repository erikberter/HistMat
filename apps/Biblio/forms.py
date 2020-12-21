from django.forms import ModelForm
from apps.Biblio.models import Book
from django import forms

class BookCreateForm(ModelForm):
    author_id = forms.IntegerField()
    class Meta:
        model = Book
        fields = ['title', 'description', 'npages', 'cover' , 'book_file', 'visibility', 'tags']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BookCreateForm, self).__init__(*args, **kwargs)

