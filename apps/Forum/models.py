from django.db import models
from .models import User
from django.urls import reverse

class post(models.Model):
    userName = models.CharField(max_length=255, default = User.get_full_name())
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum_comment', args=[self.pk])