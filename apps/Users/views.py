from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Achievement_Progress, Achievement, UserFollowing
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from .forms import ProfileForm




# Create your views here.
def user_detail(request):
    user = request.user
    progresses = Achievement_Progress.objects.filter(user = user.pk).order_by('-actual_progress')[:5]
    friends = UserFollowing.objects.filter(user_id = user.pk)[:5]
    context = {
        'user':user,
        'progresses':progresses,
        'friends': friends,
    }
    return render(request, "Users/user_detail.html", context)



class UserUpdateView(UpdateView): 
    form_class = ProfileForm
    model = Profile
    form = ProfileForm()
    template_name_suffix = '_update_form'
    success_url ='/user_detail/'

class AchievementListView(ListView):

    template_name = "Users/achievement_list.html"
    context_object_name = 'achievement_progress_list'
    model = Achievement_Progress
    paginated_by = 10

    
    def get_queryset(self):  
        user = self.request.user
        return Achievement_Progress.objects.filter(user=user.pk)
 
