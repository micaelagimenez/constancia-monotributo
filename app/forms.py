from django import forms
from .models import Monotributo

class MonotributoForm(forms.ModelForm):

    class Meta:
        model = Monotributo
        fields = ['cuit','email']