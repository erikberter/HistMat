from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


from autoslug import AutoSlugField
from taggit.managers import TaggableManager

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


class Book(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('friends','Friends Only'),
        ('public', 'Public'))

    title = models.CharField(max_length=255)
    author= models.ForeignKey(Author, on_delete=models.CASCADE,null=True, blank=True, default=None)

    publications = models.ManyToManyField(settings.AUTH_USER_MODEL)

    slug = AutoSlugField(max_length=100, unique_with=('title','author'), populate_from=custom_populate)

    book_file = models.FileField(upload_to='media/books/docs/', null=True, blank=True, default=None)

    npages = models.IntegerField()
    actpages = models.IntegerField(default=0)
    status  = models.CharField(max_length = 15, choices = VISIBILITY_CHOICES, default = 'private')

    cover = models.ImageField(upload_to='biblio/books/covers/', null=True, blank=True)

    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('biblio:book_detail',args=[self.slug])
    
# https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class BookUserDetail(models.Model):
    BOOK_STATE = (
        ('want_to_read', 'Private'),
        ('reading','Friends Only'),
        ('read', 'Public'),
        ('dropped', 'Dropped'),
        ('on_hold', 'On Hold'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    book_state =  models.CharField(max_length = 20, choices = BOOK_STATE, default = 'want_to_read')
    rating =  models.IntegerRangeField(min_value=1, max_value=10, default=5)
