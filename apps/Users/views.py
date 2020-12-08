from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Achievement_Progress, Achievement
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ProfileForm
from braces.views import UserPassesTestMixin
from django.db.models import Q
from django.http import  HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
def user_detail(request, pk):
    user = Profile.objects.get(pk = pk)
    progresses = Achievement_Progress.objects.filter(user = user.pk).filter(actual_progress__lte = 99).order_by('-actual_progress')[:3]
    friends = user.following_users.all()[:5]
    context = {
        'user_detail':user,
        'progresses':progresses,
        'friends': friends,
    }
    context['is_own_account'] = request.user == user
    if not context['is_own_account']:
        context['sigole'] = (user in request.user.following_users.all())
    
    if not progresses.exists():
        for achievement in Achievement.objects.all():
            achievement_progress = Achievement_Progress.objects.create_achievement_progress(user, achievement, 0)
            achievement_progress.save()

    return render(request, "Users/user_detail.html", context)

        
class UserUpdateView(UserPassesTestMixin, UpdateView): 
    form_class = ProfileForm
    model = Profile
    form = ProfileForm()
    template_name_suffix = '_update_form'
    success_url ='user_detail'


    def get_context_data(self,**kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['userPk'] = self.get_object().pk
        return context

    def test_func(self, user):
        is_valid = user == self.get_object()
        is_valid |= user.is_superuser
        return is_valid


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = "Users/user_delete.html"
    success_url = "/"

    def test_func(self, user):
        is_valid = user == self.get_object()
        is_valid |= user.is_superuser
        return is_valid

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
        context['is_searching'] = False
        return context

    def get_queryset(self):
        friends =  self.request.user.following_users.all()
        return friends

@require_POST
def search_view(request):
    query = request.POST.get('search')    
    context = {}
    context['user_list'] = Profile.objects.filter(username__contains=query)
    context['is_searching'] = True

    return render(request, "Users/user_list.html", context)

def seguir(request, pk):
    user = Profile.objects.get(pk = int(pk))
    a = request.user.following_users.all()
    b = a.filter(username = user.username)

    if  b.count()>0:
        request.user.following_users.remove(user)
    else:
        request.user.following_users.add(user)

    return redirect('users:user_detail', request.user.pk)