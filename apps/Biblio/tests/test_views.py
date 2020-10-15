from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User, AnonymousUser
from django.test.client import Client

from apps.Biblio.models import Book, Author

from apps.Biblio.views import catalog

class BiblioViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test_1", password="test_pass_1")
        login = self.client.login(username='test_1', password='test_pass_1')
        self.user_2 = User.objects.create_user(username="test_2", password="test_pass_2")

        self.book_public_1 = Book.objects.create(title="test_book_public_1", npages=200, status="public")
        self.book_public_1.publications.add(self.user)
        self.book_private_1 = Book.objects.create(title="test_private_book_1", npages=201, status="private")
        self.book_private_1.publications.add(self.user)
        self.book_private_2_u = Book.objects.create(title="test_private_book_2", npages=202, status="private")
        self.book_private_2_u.publications.add(self.user_2)

    ## CATALOG VIEW ##

    def test_catalog_on_user_returns_code_200(self):
        response = self.client.get('/biblio/catalog')
        self.assertEqual(response.status_code, 200)

    def test_catalog_on_anonymous_user_returns_code_200(self):
        request = self.factory.get('/biblio/catalog')
        request.user = AnonymousUser()
        response = catalog(request)
        self.assertEqual(response.status_code, 200)


    def test_catalog_on_user_contains_public_books(self):
        response = self.client.get('/biblio/catalog')
        self.assertContains(response,self.book_public_1.title)
    
    def test_catalog_on_anonymous_contains_public_book(self):
        request = self.factory.get('/biblio/catalog')
        request.user = AnonymousUser()
        response = catalog(request)

        self.assertContains(response,self.book_public_1.title)

    def test_catalog_on_anonymous_not_contains_private_book(self):
        request = self.factory.get('/biblio/catalog')
        request.user = AnonymousUser()
        response = catalog(request)

        self.assertNotIn(self.book_private_1.title, response.content.decode())
        self.assertNotIn(self.book_private_2_u.title, response.content.decode())

    def test_catalog_on_user_contains_own_private_book(self):
        response = self.client.get('/biblio/catalog')
        self.assertIn(self.book_private_1.title, response.content.decode())

    def test_catalog_on_user_not_contains_other_private_book(self):
        response = self.client.get('/biblio/catalog')
        self.assertNotIn(self.book_private_2_u.title, response.content.decode())


    def test_catalog_returns_correct_html(self):
        response = self.client.get('/biblio/catalog')

        self.assertTemplateUsed(response, 'Biblio/catalog.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_book_url_in_catalog_html(self):
        response = self.client.get('/biblio/catalog')
        self.assertContains(response, self.book_public_1.get_absolute_url())


class BookViewTest(TestCase):
    def setUp(self):
        self.example_author = Author.objects.create(name="test_name_author")
        self.example_book = Book.objects.create(title="example", npages = 200, author=self.example_author)

    def test_book_detail_contains_correct_properties(self):
        response = self.client.get(self.example_book.get_absolute_url())
        self.assertContains(response, self.example_book.title)
        self.assertContains(response, self.example_book.author)
        self.assertContains(response, self.example_book.npages)
