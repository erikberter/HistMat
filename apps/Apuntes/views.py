from django.shortcuts import render, get_object_or_404, redirect
from .models import Apunte
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApunteCreateForm
from django.http import  HttpResponseRedirect
from braces.views import UserPassesTestMixin
# Create your views here.

def apuntes(request):
    apuntes = Apunte.objects.all()
    context = {'apuntes' : apuntes}
    return render(request, 'Apuntes/apuntes.html', context)


def apuntes_detail(request, pk):
    apunte = get_object_or_404(Apunte, pk = pk)
    context = {'apunte':apunte}
    context["own_apunte"]= apunte.autor==request.user
    return render(request, 'Apuntes/apuntes_detail.html',context)



def apuntes_remove(request, pk):
    apunte = get_object_or_404(Apunte, pk=pk)
    if request.user != apunte.autor : 
        raise Http404("No eres el creador")
    apunte.delete()
    return redirect('apuntes:apuntes')
 
class ApunteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'Apuntes/forms/add_apuntes.html'
    form_class = ApunteCreateForm

    def form_valid(self, form):
        apunte = form.save()
        apunte.autor = self.request.user
        
        return HttpResponseRedirect(apunte.get_absolute_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ApunteCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class ApunteUpdateView(UserPassesTestMixin, UpdateView):
    model = Apunte
    fields = ['nombre', 'likes', 'paginas', 'documento', 'autor' , 'tamaño', 'thumbnail', 'categoria' , 'tipo']
    template_name = 'Apuntes/forms/apuntes_update.html'

    def test_func(self, user):
        return user == self.get_object().autor