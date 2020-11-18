from django.shortcuts import render
from .models import Apunte
# Create your views here.

def apuntes(request):
    apuntes = Apunte.objects.all()
    context = {'apuntes' : apuntes}
    return render(request, 'Apuntes/apuntes.html', context)


def apuntes_detail(request, pk):
    apunte = get_object_or_404(Apunte, pk = pk)
    return render(request, 'apuntes_detail.html', {'articulo':articulo})
