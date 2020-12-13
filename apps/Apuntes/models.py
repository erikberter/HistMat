from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse


class Apunte(models.Model):
    nombre = models.CharField(max_length=80)
    
    documento = models.FileField(upload_to='apuntes/docu/img')
    thumbnail = models.ImageField(upload_to = 'apuntes/docu/img/', blank = True, null = True)
    
    tipo =  models.CharField(max_length=80, default="unknown")
    likes = models.IntegerField(default=0)
    paginas = models.IntegerField(default = 0)

    autor =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    categoria = TaggableManager()
    
    def _str_(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('apuntes:apuntes_detail', args=[self.pk])

    def get_a_div(self):
        return "<a href='" + self.get_absolute_url() + "'>" + self.nombre + "</a>"
