from django.forms import ModelForm
from apps.Apuntes.models import Apunte

class ApunteCreateForm(ModelForm):
    class Meta:
        model = Apunte
        fields = ['nombre', 'documento' , 'thumbnail', 'categoria' ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ApunteCreateForm, self).__init__(*args, **kwargs)