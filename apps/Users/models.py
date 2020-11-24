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
    #actual_progress = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)


class Achievement_Progress(models.Model):
    user = models.ForeignKey('profile', on_delete=models.CASCADE, related_name='user', default=1)
    achievement = models.ForeignKey('achievement', on_delete=models.CASCADE, related_name='achievement', default=1)
    actual_progress = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' HA COMPLETADO EL ' + str(self.actual_progress) + '% DE LA TAREA ' + self.achievement.name


class Profile(AbstractUser):
    #achievements = models.ManyToManyField(Achievement, related_name='achievements')
    #achievement_progress = models.ManyToOneRel(Achievement_Progress, related_name='progresses', on_delete=models.CASCADE,field_name="achievement", to="achievement")
    profile_image = models.ImageField(upload_to='model/img/users/', blank=True, null=True)
    study_center = models.CharField(max_length=40, default = "")
    country = models.CharField(max_length=40, default = "")
    city = models.CharField(max_length=40, default = "")
    born_date = models.DateField(default=timezone.now)
    level = models.IntegerField(default=1)
    xp = models.BigIntegerField(default=0)
    kind_of_user = models.CharField(max_length=40,default="Principiante")



    def get_absolute_url(self):
        return reverse('users:user_detail')

    def get_absolute_config_url(self):
        return reverse('users:user_config', kwargs={'pk': self.pk})



class UserFollowing(models.Model):
    user_id = models.ForeignKey('profile', on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey('profile', on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return self.user_id.username + ' --> SIGUE A --> ' + self.following_user_id.username





