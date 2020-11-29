from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Achievement_Progress, Achievement
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ProfileForm


# Create your views here.
def user_detail(request):
    user = request.user
    progresses = Achievement_Progress.objects.filter(user = user.pk).filter(actual_progress__lte = 99).order_by('-actual_progress')[:2]
    friends = request.user.following_users.all()[:5]
    print(friends)
    context = {
        'user':user,
        'progresses':progresses,
        'friends': friends,
    }
    return render(request, "Users/user_detail.html", context)

def user_explore(request, pk):
    user = Profile.objects.filter(pk = pk)
    progresses = Achievement_Progress.objects.filter(user = pk).filter(actual_progress__lte = 99).order_by('-actual_progress')[:2]
    friends = request.user.following_users.all()[:5]
    context = {
        'user':user,
        'progresses':progresses,
        'friends': friends,
    }
    return render(request, "Users/user_explore.html", context)



class UserUpdateView(UpdateView): 
    form_class = ProfileForm
    model = Profile
    form = ProfileForm()
    template_name_suffix = '_update_form'
    success_url ='/user/user_detail/'


class UserDeleteView(DeleteView):
    model = Profile
    template_name = "Users/user_delete.html"
    success_url = "/"

class AchievementListView(ListView):
    template_name = "Users/achievement_list.html"
    context_object_name = 'achievement_progress_list'
    model = Achievement_Progress

    def get_queryset(self):  
        user = self.request.user
        return Achievement_Progress.objects.filter(user=user.pk)
 
class UserListView(ListView):
    template_name = "Users/user_list.html"
    context_object_name = 'user_list'
    model = Profile

    def get_context_data(self,**kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['friends'] = request.user.following_users.all()
        return context

    def get_queryset(self):
        friends =  request.user.following_users.all()
        return Profile.objects.exclude(id__in = friends)





    