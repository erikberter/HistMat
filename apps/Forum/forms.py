from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'image')

        widgets = {
            'body' : forms.Textarea(attrs={'class': 'form-control'}),
            'image' : forms.ImageField(attrs={'class': 'form-control'}),
        }