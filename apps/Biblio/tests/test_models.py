from django.test import TestCase



class AuthorModelTest(TestCase):
    def test_create_author(self):

    def test_create_empty_author(self):

    def test_repeated_author(self):

class BookModelTest(TestCase):

    def test_create_book(self):
    
    def test_create_multiple_book(self):

    def test_create_repeated_book(self):

    def test_delete_book(self):

    def test_empty_author_create(self):

    def test_create_multiple_same_author_book(self):

    def test_null_author_create(self):

class BiblioModelTest(TestCase):
    def test_create_biblio(self):

    # TODO Test on create User create biblio

    def test_add_book_to_biblio(self):

    def test_delete_book_to_biblio(self):



    