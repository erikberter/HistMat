from pinax.badges.base import Badge, BadgeAwarded
from pinax.badges.registry import badges

from apps.Biblio.models import Book

class FirstBookAddedBadge(Badge):
    slug = "first-book"
    funny = "First Book Added"
    levels = [
        "Bronze",
    ]
    events = [
        "book_added",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        first_book = Book.objects.filter(creator=user).exists()
        if first_book:
            return BadgeAwarded(level=1)


badges.register(FirstBookAddedBadge)