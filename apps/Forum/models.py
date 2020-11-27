from django.db import models
from django.urls import reverse
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, default=None)
    body = models.TextField()
    image = models.ImageField(upload_to='model/img/forum', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField()
    

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('forum:post_detail', args=[self.pk])
    
    def increaseLikes(self):
        self.likes = self.likes + 1
        return reverse('forum:post_home')

    def decreaseLikes(self):
        self.likes = self.likes - 1
        return reverse('forum:post_home')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="forum_comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, default=None)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField()

    def __str__(self):
        return self.body
    
    def increaseLikes(self):
        self.likes = self.likes + 1
        return reverse('forum:post_detail')

    def decreaseLikes(self):
        self.likes = self.likes - 1
        return reverse('forum:post_detail')