from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Achievement_Progress, Achievement
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ProfileForm
from braces.views import UserPassesTestMixin
from django.db.models import Q


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
    if request.user == user:
        context['is_own_account'] = True
    else:
        context['is_own_account'] = False
    
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

    def test_func(self, user):
        return user == self.get_object()


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = "Users/user_delete.html"
    success_url = "/"

    def test_func(self, user):
        return user == self.get_object()

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
        
        return context

    def get_queryset(self):
        friends =  self.request.user.following_users.all()
        return friends

@csrf_exempt
@require_POST
def search_view(request):
    query = request.POST.get('search')
    print(query)
    
    context = {}
    context['user_list'] = Profile.objects.filter(username__contains=query)
    print("ola")
    return render(request, "Users/user_list.html", context)
