from django.db import models
from django.conf import settings

from .action import *

from apps.Biblio.models import Book
from apps.Forum.models import *
# Create your models here.

class FriendsActionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all().exclude(visibility='private')

class PublicActionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visibility='public')

class Action(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('friends','Friends Only'),
        ('public', 'Public')
    )

    autor =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    visibility  = models.CharField(max_length = 35, choices = VISIBILITY_CHOICES, default = 'public')

    objects = models.Manager()
    public = PublicActionManager()
    friends = FriendsActionManager()

    def get_string(self, action, data, lang='es'):
        if lang not in ACTION_LIST_DICT[action]['text']:
            lang = 'es'
        return ACTION_LIST_DICT[action]['text'][lang].format(*data)

    def cast(self):
        """ Casts the object to get the original type

            Extracted from:
                - https://stackoverflow.com/questions/5225556
        """
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__):
                    return attr
            except:
                pass
        return self

    def get_dto(self, lang='es'):
        return {'autor' : self.autor, 'text' : self.cast().get_string(lang = lang) , 'timestamp' : self.creado}

class ActionBookAdd(Action):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('book_add', [self.autor.get_a_div(), self.book.get_a_div()] , lang)


class ActionBookState(Action):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, blank=True)

    def get_string(self, lang='es'):
        return super().get_string('book_state', [self.autor.get_a_div(), self.book.get_a_div(), self.status] , lang)

class ActionBookRate(Action):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    valoracion = models.IntegerField(default = 0)

    def get_string(self, lang='es'):
        return super().get_string('book_rate', [self.autor.get_a_div(), self.book.get_a_div(), self.valoracion] , lang)


class ActionBookPageChange(Action):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page = models.IntegerField(default = 0)

    def get_string(self, lang='es'):
        return super().get_string('book_page_change', [self.autor.get_a_div(), self.book.get_a_div(), self.page] , lang)

class ActionPostAdd(Action):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('post_add', [self.autor.get_a_div(), self.post.get_a_div()] , lang)


class ActionPostComment(Action):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('post_comment', [self.autor.get_a_div(), self.post.get_a_div(), self.comment.body[:255]] , lang)

class ActionPostLike(Action):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('post_like', [self.autor.get_a_div(), self.post.get_a_div()] , lang)

