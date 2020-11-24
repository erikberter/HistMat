from .models import Profile
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Reset, Row, Column, ButtonHolder


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('profile_image','study_center', 'country', 'city','born_date')
        

    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('submit', 'save'))



    
  






