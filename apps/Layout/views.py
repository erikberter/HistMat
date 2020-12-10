from django.shortcuts import render

from apps.UserMechanics.models import Action 

# Create your views here.
def index(request):
    context = {}

    return render(request, 'index.html', context)
import time
def home(request):
    context = {}
    start = time.time()
    lang = request.LANGUAGE_CODE
    context['action_list'] = [ {'autor' : obj.autor, 'text' : obj.cast().get_string(lang = lang) , 'timestamp' : obj.creado} for obj in Action.objects.order_by('-creado')[:10]]
    end = time.time()
    print("----------------")
    print(end - start)
    print("---------------")
    return render(request, 'home.html', context)