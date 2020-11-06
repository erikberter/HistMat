from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings



# Create your models here.
'''
class User(models.Model):
    username = models.CharField(max_length=40, default = "")
    name = models.CharField(max_length=40, default = "")
    surname = models.CharField(max_length=60, default = "")

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.pk])
'''

from django.contrib.auth.models import AbstractUser


class UserData(models.Model):
    
    profile_image = models.ImageField(upload_to='model/img/users/', blank=True, null=True)
    study_center = models.CharField(max_length=40, default = "")
    country = models.CharField(max_length=40, default = "")
    city = models.CharField(max_length=40, default = "")
    born_date = models.DateField(default=timezone.now)

    
    
    

class UserRol(models.Model):
    
    level = models.IntegerField(default=1)
    xp = models.BigIntegerField(default=0)
    kind_of_user = models.CharField(max_length=40,default="Principiante")


class Achievement(models.Model):
    name = models.CharField(max_length=40, default = "")
    achievement_image = models.ImageField(upload_to='media/model/img/achievements/', blank=True, null=True)
    description = models.TextField(default="")
    funny_phrase = models.CharField(max_length=40,default="")
    xp_cuantity = models.BigIntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)


def default_detail_object():
    return UserData.objects.create()

def default_rol_object():
    return UserRol.objects.create()


class Profile(AbstractUser):
    detail = models.ForeignKey(UserData, on_delete=models.CASCADE, default=default_detail_object,related_name="detail")
    rol = models.ForeignKey(UserRol, on_delete=models.CASCADE, default=default_rol_object, related_name="rol")

    def get_absolute_url(self):
        return reverse('users:user_detail')
    
