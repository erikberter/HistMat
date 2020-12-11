from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from sorl.thumbnail import get_thumbnail
from django.core.files.base import ContentFile

from .badges import *


level_name_relation = ['Principiante','Novato','Aprendiz','Jugador','Experto','Dios','Stalin']

class Profile(AbstractUser):
    #-----------------PERDONAL DATA------------------------------
    profile_image = models.ImageField(upload_to='model/img/users/', blank=True, null=True)
    profile_image_t11 = models.ImageField(upload_to='model/img/users_t11/', null=True, blank=True)

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

    is_content_editor = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.pk})

    def get_absolute_config_url(self):
        return reverse('users:user_config', kwargs={'pk': self.pk})
    
    def get_level_progress(self):
        progress = self.xp // self.get_level_max_xp()
        return progress
    
    def get_level_max_xp(self):
        return self.level*10

    def get_a_div(self):
        return "<a href='" + self.get_absolute_url() + "'>" + self.username + "</a>"
    
    def add_exp(self, xp):
        self.xp += xp
        while self.xp > self.level*10:
            self.xp -= self.level*10
            self.level += 1
            if self.level % 10 == 0 and self.level < 65:
                self.kind_of_user = level_name_relation[self.level // 10]

        self.save()

class ProfileStats(models.Model):
    user = models.ForeignKey('profile', on_delete=models.CASCADE, related_name='user_stats', default=1)
    like_counter = models.IntegerField(default=0)
    view_counter = models.IntegerField(default=0)
    book_upload_counter = models.IntegerField(default=0)
    book_readed_counter = models.IntegerField(default=0)
    following_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' STATS '





