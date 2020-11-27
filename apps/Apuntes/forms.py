from django.forms import ModelForm, Form
from apps.Apuntes.models import Apunte

class ApunteCreateForm(ModelForm):
    class Meta:
        model = Apunte
        fields = ['nombre', 'likes', 'paginas', 'documento', 'autor' , 'tamaño', 'thumbnail', 'categoria' , 'tipo']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ApunteCreateForm, self).__init__(*args, **kwargs)