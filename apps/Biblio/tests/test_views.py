from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User, AnonymousUser
from django.test.client import Client

from apps.Biblio.models import Book, Author

from apps.Biblio.views import catalog, book_detail

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

    ###  BOOK_DETAIL VIEW  ###

    def test_user_access_book_detail_returns_200_on_public_book(self):
        response = self.client.get(self.book_public_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.book_public_1.title)
    
    def test_user_access_book_detail_returns_200_on_own_private_book(self):
        response = self.client.get(self.book_private_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.book_private_1.title)

    def test_user_access_book_detail_returns_404_on_not_own_private_book(self):
        response = self.client.get(self.book_private_2_u.get_absolute_url())
        self.assertEqual(response.status_code, 404)
    
    def test_anonymous_access_book_detail_returns_200_on_public_book(self):
        request = self.factory.get(self.book_public_1.get_absolute_url())
        request.user = AnonymousUser()
        response = book_detail(request, self.book_public_1.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.book_public_1.title)
    
    def test_anonymous_access_book_detail_returns_404_on_private_book(self):
        request = self.factory.get(self.book_private_1.get_absolute_url())
        request.user = AnonymousUser()
        response = book_detail(request,self.book_private_1.slug)
        self.assertEqual(response.status_code, 404, "Error on 'own' book")

        request = self.factory.get(self.book_private_2_u.get_absolute_url())
        request.user = AnonymousUser()
        response = book_detail(request,self.book_private_2_u.slug )
        self.assertEqual(response.status_code, 404, "Error on external book")

    def test_book_detail_contains_correct_properties(self):
        response = self.client.get(self.book_public_1.get_absolute_url())
        self.assertContains(response, self.book_public_1.title)
        self.assertContains(response, self.book_public_1.author)
        self.assertContains(response, self.book_public_1.npages)