from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from autoslug import AutoSlugField
from taggit.managers import TaggableManager

from django.conf import settings

from .external import IntegerRangeField


#################################
#        Helper Functions       #
#################################

def custom_populate(instance):
    """
        Custom populate function for the book slug.
    """
    if not instance.author:
        return f"{instance.title}_anonymous"
    return f"{instance.title}_{instance.author.name}"


#################################
#             Models            #
#################################


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    surname = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        if self.surname:
            return self.name+" "+self.surname
        else:
            return self.name

class PublicBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visibility='public')

class Book(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('friends','Friends Only'),
        ('public', 'Public')
    )

    #################################################
    #                   Book Details                #
    #################################################
    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    
    # TODO Adapt to better handling model
    npages = models.IntegerField()

    book_file = models.FileField(upload_to='biblio/books/docs/', null=True, blank=True, default=None)
    cover = models.ImageField(upload_to='biblio/books/covers/', null=True, blank=True)

    #################################################
    #               Book Metadata                   #
    #################################################
    slug = AutoSlugField(max_length=100, unique_with=('title','author'), populate_from=custom_populate)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    visibility  = models.CharField(max_length = 35, choices = VISIBILITY_CHOICES, default = 'private')

    tags = TaggableManager()

    objects = models.Manager()
    public = PublicBookManager()

    #################################################
    #               Book Relationships              #
    #################################################
    
    author= models.ForeignKey(Author, on_delete=models.SET_NULL,null=True, blank=True, default=None, related_name="books")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BookUserDetail', related_name='users')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, default=None)

    class Meta:
        ordering = ['updated']

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('biblio:book_detail',args=[self.slug])

    def get_dto(self):
        """
            Data Transfer Object assembler function.
            Returns a dictionary with the data for the webpage. 
        """
        data = {}

        data["title"] = self.title
        data["description"] = self.description
        data["author"] = self.author.__str__()
        data["created"] = self.created
        data["slug"] = self.slug

        data["detail_url"] = self.get_absolute_url()

        data["tags"] = []
        for tag in self.tags.all():
            data["tags"].append(tag.name)
        
        if self.book_file:
            data["file_url"] = self.book_file.url
        else:
            data["file_url"] = ""


        if self.cover:
            data["cover_url"] = self.cover.url
        else:
            data["cover_url"] = ""
        
        return data


class BookUserDetail(models.Model):
    """
        Sumary: This class is the relation between a user and a book which holds the 
        user current state within the book.
    """

    BOOK_STATE = (
        ('want_to_read', 'Want to Read'),
        ('reading','Reading'),
        ('read', 'Read'),
        ('dropped', 'Dropped'),
        ('on_hold', 'On Hold'))
    BOOK_STATE_L = [t[0] for t in BOOK_STATE]

    DEFAULT_BOOK_STATE = "want_to_read"


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


    rating =  IntegerRangeField(min_value=1, max_value=10, null=True, blank=True)
    book_state =  models.CharField(max_length = 30, choices = BOOK_STATE, default = DEFAULT_BOOK_STATE)
    act_page = models.IntegerField(default=0)
    

    #tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.__str__() + self.book.__str__()

    def get_dto(self):
        """
            Data Transfer Object assembler function.
            Returns a dictionary with the data for the webpage. 
        """
        data = {}

        data["rating"] = self.rating
        data["book_state"] = self.book_state
        data["created"] = self.created
        data["act_page"] = self.act_page