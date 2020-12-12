from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils import timezone


class Apunte(models.Model):
    nombre = models.CharField(max_length=80)
    likes = models.IntegerField(default=0)
    paginas = models.IntegerField(default = 0)
    documento = models.FileField(upload_to='apuntes/docu/img')
    autor =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to = 'apuntes/docu/img/', blank = True, null = True)
    categoria = TaggableManager()
    tipo =  models.CharField(max_length=80, default="unknown")
    creado = models.DateTimeField(default=timezone.now)
    editado = models.DateTimeField(default=timezone.now)
    
    
    def _str_(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('apuntes:apuntes_detail', args=[self.pk])

    def get_a_div(self):
        html = ""
        html += "<a href='" + self.get_absolute_url() + "'>" + self.nombre + "</a>"
        
        return html
