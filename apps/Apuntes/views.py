from django.shortcuts import render
from .models import Apunte
# Create your views here.

def apuntes(request):
    apuntes = Apunte.objects.all()
    context = {'apuntes' : apuntes}
    return render(request, 'Apuntes/apuntes.html', context)


