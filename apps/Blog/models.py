from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse

from autoslug import AutoSlugField

class Blog(models.Model):
    title = models.CharField(max_length=80, default = "")
    text = models.TextField(default = "")
    likes = models.PositiveIntegerField(default=0)
    autor =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to = 'apuntes/docu/img/', blank = True, null = True)
    slug = AutoSlugField(max_length=100, unique=True, populate_from='title')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['updated']

    def _str_(self):
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.slug])

