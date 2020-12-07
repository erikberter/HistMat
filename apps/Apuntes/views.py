from django.shortcuts import render, get_object_or_404, redirect
from .models import Apunte

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApunteCreateForm
from django.http import  HttpResponseRedirect
from braces.views import UserPassesTestMixin

import os
# Create your views here.

class ApuntesListView(ListView):
    model = Apunte
    template_name = 'Apuntes/apuntes.html'
    context_object_name = "apuntes"

    paginate_by = 10

class ApuntesDetailView(DetailView):
    model = Apunte
    context_object_name = "apunte"
    template_name = 'Apuntes/apuntes_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["own_apunte"]= self.get_object().autor==self.request.user
        return data



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
        apunte = form.save(commit = False)
        apunte.autor = self.request.user
        name, extension = os.path.splitext(apunte.documento.path)
        apunte.tipo = extension
        apunte.save()
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