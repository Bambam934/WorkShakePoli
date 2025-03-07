from django import forms
from .models import Inicio

class InicioSesionForm(forms.ModelForm):  # Cambio de nombre para evitar confusión
    class Meta:
        model = Inicio
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
  
  
    