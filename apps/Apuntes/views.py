from django.shortcuts import render, get_object_or_404
from .models import Apunte
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApunteCreateForm
# Create your views here.

def apuntes(request):
    apuntes = Apunte.objects.all()
    context = {'apuntes' : apuntes}
    return render(request, 'Apuntes/apuntes.html', context)


def apuntes_detail(request, pk):
    apunte = get_object_or_404(Apunte, pk = pk)
    return render(request, 'Apuntes/apuntes_detail.html', {'apunte':apunte})


class ApunteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'Apuntes/forms/add_apuntes.html'
    form_class = ApunteCreateForm

    def form_valid(self, form):
        apunte = apunte.save()
        apunte.autor = self.request.user
        
        return HttpResponseRedirect(apunte.get_absolute_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ApunteCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
