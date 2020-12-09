from django.shortcuts import render

from apps.UserMechanics.models import Action 

# Create your views here.
def index(request):
    context = {}

    return render(request, 'index.html', context)

def home(request):
    context = {}
    context['action_list'] = [ { 'text' : obj.cast().get_string() , 'timestamp' : obj.creado} for obj in Action.objects.order_by('creado')[:20]]
    return render(request, 'home.html', context)