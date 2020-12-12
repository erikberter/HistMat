from django.db import models
from django.urls import reverse
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, default=None)
    title = models.CharField(max_length=70)
    body = models.TextField()
    image = models.ImageField(upload_to='model/img/forum', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('forum:post_detail', args=[self.pk])

    def get_a_div(self):
        html = ""
        html += "<a href='" + self.get_absolute_url() + "'>" + self.body[:50] + "</a>"
        
        return html

    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="forum_comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, default=None)
    parent = models.ForeignKey('self', related_name="childs", null=True, default=None, on_delete=models.SET_NULL)

    body = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.user.username