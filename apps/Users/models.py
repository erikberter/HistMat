from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser




# Create your models here.
'''
class User(models.Model):
    username = models.CharField(max_length=40, default = "")
    name = models.CharField(max_length=40, default = "")
    surname = models.CharField(max_length=60, default = "")

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.pk])
'''



class Achievement(models.Model):
    name = models.CharField(max_length=40, default = "")
    achievement_image = models.ImageField(upload_to='media/model/img/achievements/', blank=True, null=True)
    description = models.TextField(default="")
    funny_phrase = models.CharField(max_length=40,default="")
    xp_cuantity = models.BigIntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)


class Achievement_Progress(models.Model):
    user = models.ForeignKey('profile', on_delete=models.CASCADE, related_name='user', default=1)
    achievement = models.ForeignKey('achievement', on_delete=models.CASCADE, related_name='achievement', default=1)
    actual_progress = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' HA COMPLETADO EL ' + str(self.actual_progress) + '% DE LA TAREA ' + self.achievement.name


class Profile(AbstractUser):
    #-----------------PERDONAL DATA------------------------------
    profile_image = models.ImageField(upload_to='model/img/users/', blank=True, null=True)
    study_center = models.CharField(max_length=40, default = "", blank=True)
    country = models.CharField(max_length=40, default = "", blank=True)
    city = models.CharField(max_length=40, default = "", blank=True)
    born_date = models.DateField(default=timezone.now)
    #--------------------SOCIAL------------------------------
    website = models.CharField(max_length=40, default = "", null=True, blank=True)
    github = models.CharField(max_length=40, default = "",  null=True, blank=True)
    instagram = models.CharField(max_length=40, default = "",  null=True, blank=True)
    twitter = models.CharField(max_length=40, default = "", null=True, blank=True)
    facebook = models.CharField(max_length=40, default = "",  null=True, blank=True)
    #--------------------LEVEL------------------------------
    level = models.IntegerField(default=1)
    xp = models.BigIntegerField(default=0)
    kind_of_user = models.CharField(max_length=40,default="Principiante")

    following = models.ManyToManyField('profile', related_name='following_users')

    def get_absolute_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.pk})

    def get_absolute_config_url(self):
        return reverse('users:user_config', kwargs={'pk': self.pk})
 

class ProfileStats(models.Model):
    user = models.ForeignKey('profile', on_delete=models.CASCADE, related_name='user_stats', default=1)
    like_counter = models.IntegerField(default=0)
    view_counter = models.IntegerField(default=0)
    book_upload_counter = models.IntegerField(default=0)
    book_readed_counter = models.IntegerField(default=0)
    following_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' STATS '





