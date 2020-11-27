from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.urls import reverse

class Apunte(models.Model):
    nombre = models.CharField(max_length=80)
    likes = models.IntegerField()
    paginas = models.IntegerField()
    documento = models.FileField(upload_to='apuntes/docu/img')
    autor =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tamaño = models.IntegerField()
    thumbnail = models.ImageField(upload_to = 'apuntes/docu/img/', blank = True, null = True)
    categoria = TaggableManager()
    tipo =  models.CharField(max_length=80)
    creado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(auto_now_add=True)
    
    
    def _str_(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('apuntes:apuntes_detail', args=[self.pk])


#class AddApunte(CreateView):
    # model = Apunte
    # template_name = 'add_apuntes.html'
    # fields = '__all__'
    # success_url = reverse_lazy('apuntes')  