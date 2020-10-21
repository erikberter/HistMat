from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser

from apps.Biblio.models import *

class AuthorModelTest(TestCase):
    def test_create_author(self):
        autor_test_1 = Author.objects.create(name="test_name", surname="test_surname")
        self.assertEqual(autor_test_1.name,"test_name")
        self.assertEqual(autor_test_1.surname,"test_surname")
        self.assertEqual(Author.objects.count(),1)

    def test_create_multiple_author(self):
        autor_test_1 = Author.objects.create(name="test_name", surname="test_surname")
        autor_test_2 = Author.objects.create(name="test_name_2", surname="test_surname_2")
        self.assertEqual(Author.objects.count(),2)
        self.assertEqual(list(Author.objects.all()), [autor_test_1, autor_test_2])

    def test_create_empty_author(self):
        try:
            autor_test_1 = Author.objects.create()
            self.fail("Author name cannot be empty")
        except:
            pass

class BookModelTest(TestCase):

    def setUp(self):
        self.author_test_1 = Author.objects.create(name="test_name", surname="test_surname")

    def test_create_book(self):
        book_test_1 = Book.objects.create(title="test_title_1", npages=200)
        self.assertEqual(Book.objects.first(), book_test_1)
        self.assertEqual(book_test_1.title, "test_title_1")
        self.assertEqual(book_test_1.npages, 200)
        self.assertEqual(book_test_1.visibility, "private")

    
    def test_create_multiple_book(self):
        book_test_1 = Book.objects.create(title="test_title_1", npages=200)
        book_test_2 = Book.objects.create(title="test_title_2", npages=200)
        self.assertEqual(list(Book.objects.all()), [book_test_1, book_test_2])

    def test_book_with_author_create(self):
        book_test_1 = Book.objects.create(title="test_title_1", npages=200, author=self.author_test_1)
        self.assertEqual(book_test_1.author, self.author_test_1)
    
    def test_create_multiple_same_author_book(self):
        book_test_1 = Book.objects.create(title="test_title_1", npages=200, author=self.author_test_1)
        book_test_2 = Book.objects.create(title="test_title_2", npages=200, author=self.author_test_1)
        book_test_3 = Book.objects.create(title="test_title_2", npages=200)
        self.assertEqual(list(Book.objects.filter(author=self.author_test_1)), [book_test_1, book_test_2])
        self.assertEqual(Book.objects.count(), 3)
    
    def test_book_get_absolute_path(self):
        book_test_1 = Book.objects.create(title="test_title_1", npages=200, author=self.author_test_1)
        self.assertEquals('/biblio/book_detail/' + book_test_1.title+'_' + book_test_1.author.name, book_test_1.get_absolute_url())

class BookUserDetailTest(TestCase):
    def setUp(self):
        self.author_test_1 = Author.objects.create(name="test_name", surname="test_surname")
        self.book_test_1 = Book.objects.create(title="test_title_1", npages=200, author=self.author_test_1)
        self.user = User.objects.create_user(username="test_1", password="test_pass_1")
    
    def test_create_book_user_detail(self):
        self.book_user_detail_test = BookUserDetail.objects.create(user=self.user, book=self.book_test_1)
        self.assertEqual(self.book_user_detail_test.user, self.user)
        self.assertEqual(self.book_user_detail_test.book, self.book_test_1)
    
    def test_queryset_to_book_values(self):
        self.book_user_detail_test = BookUserDetail.objects.create(user=self.user, book=self.book_test_1)
        book1 = BookUserDetail.objects.filter(user=self.user, book=self.book_test_1).first()
        self.assertEqual(book1.book, self.book_test_1)