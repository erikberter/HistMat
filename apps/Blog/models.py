from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils import timezone


class Blog(models.Model):
    nombre = models.CharField(max_length=80)
    likes = models.PositiveIntegerField(default=0)
    autor =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to = 'apuntes/docu/img/', blank = True, null = True)
    

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['updated']

    def _str_(self):
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('apuntes:apuntes_detail', args=[self.pk])

    def get_a_div(self):
        html = ""
        html += "<a href='" + self.get_absolute_url() + "'>" + self.nombre + "</a>"
        
        return html
