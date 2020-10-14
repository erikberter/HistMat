

def BiblioViewTest(TestCase):
    def test_catalog_contains_books(self):


def BookViewTest(TestCase):

    def test_book_detail_contains_correct_properties(self):
        response = self.client.get(self.example_book.get_absolute_url())
        self.assertContains(self.example_book.title, response)
        self.assertContains(self.example_book.author, response)
