from django.db import models
from django.conf import settings
from django.utils import timezone

from autoslug import AutoSlugField
from taggit.managers import TaggableManager

class Author(models.Model):
    name = models.CharField(max_length=100)


def custom_slugify(value):
    value = value.replace(':','-')
    value = value.replace('.','-')
    value = value.replace(',','-')
    value = value.replace(' ','-')
    return value

class Book(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('friends','Friends Only'),
        ('public', 'Public'))

    title = models.CharField(max_length=255)
    author= models.ForeignKey(Author, on_delete=models.CASCADE,null=True, blank=True, default=None)

    publications = models.ManyToManyField(settings.AUTH_USER_MODEL)

    slug = AutoSlugField(max_length=50, unique_for_date='publish', populate_from='title', 
                        slugify=custom_slugify)

    npages = models.IntegerField()
    actpages = models.IntegerField(default=0)
    status  = models.CharField(max_length = 10, choices = VISIBILITY_CHOICES, default = 'private')

    img = models.ImageField(upload_to='biblio/books/covers/', null=True, blank=True)

    publish = models.DateTimeField(default=timezone.now)

    


