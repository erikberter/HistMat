from django.db import models
from django.conf import settings

from .action import *

from apps.Biblio.models import Book
from apps.Apuntes.models import Apunte
from apps.Forum.models import *
# Create your models here.


class Action(models.Model):
    autor =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def get_string(self, action, data, lang='es'):
        return ACTION_LIST_DICT[action]['text'][lang].format(*data)

    def cast(self):
        """ Casts the object to get the original type

            Extracted from:
                - https://stackoverflow.com/questions/5225556/determining-django-model-instance-types-after-a-query-on-a-base-class
        """
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__):
                    return attr
            except:
                pass
        return self

class ActionBookAdd(Action):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('book_add', [self.autor.get_a_div(), self.book.title] , lang)

class ActionBookRate(Action):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    valoracion = models.IntegerField(default = 0)

    def get_string(self, lang='es'):
        return super().get_string('book_rate', [self.autor.get_a_div(), self.book.title, self.valoracion] , lang)


class ActionBookPageChange(Action):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page = models.IntegerField(default = 0)

    def get_string(self, lang='es'):
        return super().get_string('book_page_change', [self.autor.get_a_div(), self.book.title, self.page] , lang)

class ActionPostAdd(Action):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('post_add', [self.autor.get_a_div(), self.post.body[:255]] , lang)


class ActionPostComment(Action):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('post_comment', [self.autor.get_a_div(), self.post.body[:255], self.comment.body[:255]] , lang)

class ActionPostLike(Action):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('post_like', [self.autor.get_a_div(), self.post.body[:255]] , lang)

class ActionApunteAdd(Action):
    apunte = models.ForeignKey(Book, on_delete=models.CASCADE)

    def get_string(self, lang='es'):
        return super().get_string('apunte_add', [self.autor.get_a_div(), self.nombre] , lang)
