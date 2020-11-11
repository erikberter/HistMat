from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.


def user_detail(request):
    user = request.user
 
    context = {
        'user':user,
    }
    return render(request, "Users/user_detail.html", context)