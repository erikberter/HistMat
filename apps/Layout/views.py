from django.shortcuts import render
from django.shortcuts import redirect

from apps.UserMechanics.models import Action 

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def home(request):
    if not request.user.is_authenticated:
        return redirect("layout:index")

    context = {}
    lang = request.LANGUAGE_CODE

    followings = request.user.following_users.all()
    context['action_list'] = [ obj.get_dto(lang)  for obj in Action.friends.filter(autor__in=followings).order_by('-creado')[:10] ]
    return render(request, 'home.html', context)

def contacts(request):
    return render(request, 'Contact/contact.html', {})