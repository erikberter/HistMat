from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ProfileForm
from braces.views import UserPassesTestMixin
from django.db.models import Q
from django.http import  HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from sorl.thumbnail import get_thumbnail

# Create your views here.
def user_detail(request, pk):
    user = Profile.objects.get(pk = pk)
    friends = user.following_users.all()[:5]
    
    context['is_own_account'] = request.user == user
    if not context['is_own_account']:
        context['sigole'] = request.user.following_users.filter(username=user.username).exists()
    

    return render(request, "Users/user_detail.html", {'user_detail':user, 'friends': friends})

        
class UserUpdateView(UserPassesTestMixin, UpdateView): 
    form_class = ProfileForm
    model = Profile
    form = ProfileForm()
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        redirect_url = super(UserUpdateView, self).form_valid(form)
        
        if form.instance.profile_image:
            self.request.user.profile_image_t11 = get_thumbnail(
                form.instance.profile_image,
                '100x100',
                crop='center',
                quality=80).name
        self.request.user.save()

        return HttpResponseRedirect(user.get_absolute_url())

    def get_context_data(self,**kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['userPk'] = self.get_object().pk
        return context

    def test_func(self, user):
        return ( user == self.get_object() ) | user.is_superuser


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = "Users/user_delete.html"
    success_url = "/"

    def test_func(self, user):
        return ( user == self.get_object() ) | user.is_superuser 
 
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
    followins = request.user.following_users.all()

    if  followins.filter(id = user.id).exists():
        request.user.following_users.remove(user)
    else:
        request.user.following_users.add(user)

    return redirect('users:user_detail', request.user.pk)