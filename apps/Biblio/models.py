from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from autoslug import AutoSlugField
from taggit.managers import TaggableManager

# https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    surname = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        if self.surname:
            return self.name+" "+self.surname
        else:
            return self.name

def custom_populate(instance):
    if not instance.author:
        return f"{instance.title}_anonymous"
    return f"{instance.title}_{instance.author.name}"

class PublicBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visibility='public')

class Book(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('friends','Friends Only'),
        ('public', 'Public')
    )

    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    author= models.ForeignKey(Author, on_delete=models.CASCADE,null=True, blank=True, default=None)

    slug = AutoSlugField(max_length=100, unique_with=('title','author'), populate_from=custom_populate)

    npages = models.IntegerField()


    book_file = models.FileField(upload_to='biblio/books/docs/', null=True, blank=True, default=None)
    cover = models.ImageField(upload_to='biblio/books/covers/', null=True, blank=True)
    
    users = models.ManyToManyField(User, through='BookUserDetail', related_name='users')
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=None)

    visibility  = models.CharField(max_length = 35, choices = VISIBILITY_CHOICES, default = 'private')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    objects = models.Manager()
    public = PublicBookManager()

    class Meta:
        ordering = ['updated']

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('biblio:book_detail',args=[self.slug])


class BookRating(models.Model):
    rating =  IntegerRangeField(min_value=1, max_value=10, default=5)

class BookUserDetail(models.Model):
    BOOK_STATE = (
        ('want_to_read', 'Want to Read'),
        ('reading','Reading'),
        ('read', 'Read'),
        ('dropped', 'Dropped'),
        ('on_hold', 'On Hold'))
    BOOK_STATE_L = [t[0] for t in BOOK_STATE]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.ForeignKey(BookRating, null=True, blank=True, on_delete=models.CASCADE)
    book_state =  models.CharField(max_length = 20, choices = BOOK_STATE, default = 'want_to_read')
    act_page = models.IntegerField(default=0)
    

    tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.__str__() + self.book.__str__()
