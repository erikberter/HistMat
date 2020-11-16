from django.db import models
from .models import User
from django.urls import reverse

class Post(models.Model):
    userName = models.CharField(max_length=255, default = User.get_full_name())
    body = models.TextField()
    image = models.ImageField(upload_to='model/img/users/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField()

    def __str__(self):
        return self.userName

    def get_absolute_url(self):
        return reverse('forum_post', args=[self.pk])

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="forum_comments", on_delete=models.CASCADE)
    userName = models.CharField(max_length=255, default = User.get_full_name())
    body = models.TextField()
    likes = models.PositiveIntegerField()

    def __str__(self):
        return self.userName