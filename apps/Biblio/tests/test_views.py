from django.test import TestCase, RequestFactory
from django.http import Http404
from django.contrib.auth.models import User, AnonymousUser
from django.test.client import Client

from apps.Biblio.models import Book, Author, BookUserDetail

from apps.Biblio.views import CatalogView, book_detail


DEFAULT_MYBOOKS_DATA = {
    "search_book" : "",
    "book_state" : "want_to_read",
    "book_order" : "last_added"
    }

AYAX_COM = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

class BiblioViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test_1", password="test_pass_1")
        login = self.client.login(username='test_1', password='test_pass_1')
        self.user_2 = User.objects.create_user(username="test_2", password="test_pass_2")

        self.book_public_1 = Book.objects.create(title="test_book_public_1", npages=200, visibility="public")
        self.book_public_1_BUD = BookUserDetail.objects.create(user = self.user, book=self.book_public_1, book_state="want_to_read")

        self.book_private_1 = Book.objects.create(title="test_private_book_1", npages=201, visibility="private")
        self.book_private_1_BUD = BookUserDetail.objects.create(user = self.user, book=self.book_private_1, book_state="want_to_read")

        self.book_private_1_r = Book.objects.create(title="test_private_book_1_r", npages=201, visibility="private")
        self.book_private_1_r_BUD = BookUserDetail.objects.create(user = self.user, book=self.book_private_1_r, book_state="reading")

        self.book_private_2_u = Book.objects.create(title="test_private_book_2", npages=202, visibility="private")
        self.book_private_2_u_BUD = BookUserDetail.objects.create(user = self.user_2, book=self.book_private_2_u, book_state="want_to_read")

        self.book_public_3_u = Book.objects.create(title="test_public_book_3", npages=202, visibility="public")
        self.book_public_3_u_BUD = BookUserDetail.objects.create(user = self.user_2, book=self.book_public_3_u, book_state="want_to_read")

    

    ## catalog VIEW ##

    def test_catalog_public_returns_200(self):
        response = self.client.get('/biblio/public/catalog')
        self.assertEqual(response.status_code, 200)
    
    def test_catalog_public_on_anonymous_user_returns_code_200(self):
        request = self.factory.get('/biblio/public/catalog')
        request.user = AnonymousUser()
        response = CatalogView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_catalog_public_on_user_contains_public_books(self):
        response = self.client.get('/biblio/public/catalog')
        self.assertContains(response,self.book_public_1.title)
        self.assertContains(response,self.book_public_3_u.title)
    
    def test_catalog_public_on_anonymous_contains_public_book(self):
        request = self.factory.get('/biblio/public/catalog')
        request.user = AnonymousUser()
        response = CatalogView.as_view()(request)

        self.assertContains(response,self.book_public_1.title)
        self.assertContains(response,self.book_public_3_u.title)

    def test_catalog_public_contains_book_url(self):
        response = self.client.get('/biblio/public/catalog')
        self.assertContains(response,self.book_public_1.get_absolute_url())

    def test_catalog_public_not_contains_private_book(self):
        response = self.client.get('/biblio/public/catalog')

        self.assertNotIn(self.book_private_1.title, response.content.decode())
        self.assertNotIn(self.book_private_2_u.title, response.content.decode())

    def test_catalog_public_on_anonymous_not_contains_private_book(self):
        request = self.factory.get('/biblio/public/catalog')
        request.user = AnonymousUser()
        response = CatalogView.as_view()(request)

        self.assertNotContains(response,self.book_private_1.title)
        self.assertNotContains(response,self.book_private_2_u.title)


    def test_catalog_returns_correct_html(self):
        response = self.client.get('/biblio/public/catalog')

        self.assertTemplateUsed(response, 'Biblio/catalog.html')
        self.assertTemplateUsed(response, 'base.html')

    ###  MYBOOKS ###
    ### We won't check for anonymous users since we have the Django login_required decorator
    ### All the tests happend with a logged client

    def test_mycatalog_returns_200(self):
        response = self.client.get('/biblio/mycatalog')
        self.assertEqual(response.status_code, 200)

    def test_mycatalog_contains_own_public_book(self):
        response = self.client.post('/biblio/mycatalog', DEFAULT_MYBOOKS_DATA, **AYAX_COM)
        self.assertIn(self.book_public_1.title, response.content.decode())

    def test_mycatalog_contains_own_private_book(self):
        response = self.client.post('/biblio/mycatalog', DEFAULT_MYBOOKS_DATA, **AYAX_COM)
        self.assertIn(self.book_private_1.title, response.content.decode())

    def test_mycatalog_not_contains_other_private_book(self):
        response = self.client.post('/biblio/mycatalog', DEFAULT_MYBOOKS_DATA, **AYAX_COM)
        self.assertNotIn(self.book_private_2_u.title, response.content.decode())

    def test_mycatalog_not_contains_other_public_book(self):
        response = self.client.post('/biblio/mycatalog', DEFAULT_MYBOOKS_DATA, **AYAX_COM)
        self.assertNotIn(self.book_public_3_u.title, response.content.decode())

    def test_mycatalog_on_want_to_read_not_contains_reading_book(self):
        response = self.client.post('/biblio/mycatalog', DEFAULT_MYBOOKS_DATA, **AYAX_COM)
        self.assertNotIn(self.book_private_1_r.title, response.content.decode())


    def test_mycatalog_returns_correct_html(self):
        response = self.client.get('/biblio/mycatalog')

        self.assertTemplateUsed(response, 'Biblio/mycatalog.html')
        self.assertTemplateUsed(response, 'base.html')
    
    def test_mycatalog_contains_book_url(self):
        response = self.client.post('/biblio/mycatalog', DEFAULT_MYBOOKS_DATA, **AYAX_COM)
        self.assertContains(response, self.book_public_1.get_absolute_url())
        self.assertContains(response, self.book_private_1.get_absolute_url())




    ###  BOOK_DETAIL VIEW  ###

    def test_user_access_book_detail_returns_200_on_public_self_book(self):
        response = self.client.get(self.book_public_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.book_public_1.title)

    def test_user_access_book_detail_returns_200_on_public_other_user_book(self):
        response = self.client.get(self.book_public_3_u.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.book_public_3_u.title)

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

        request = self.factory.get(self.book_public_3_u.get_absolute_url())
        request.user = AnonymousUser()
        response = book_detail(request, self.book_public_3_u.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.book_public_3_u.title)
    
    def test_anonymous_access_book_detail_returns_404_on_private_book(self):
        request = self.factory.get(self.book_private_1.get_absolute_url())
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            book_detail(request,self.book_private_1.slug)
        

        request = self.factory.get(self.book_private_2_u.get_absolute_url())
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            book_detail(request,self.book_private_2_u.slug )

    def test_book_detail_contains_correct_properties(self):
        response = self.client.get(self.book_public_1.get_absolute_url())
        self.assertContains(response, self.book_public_1.title)
        self.assertContains(response, self.book_public_1.author)
        self.assertContains(response, self.book_public_1.npages)