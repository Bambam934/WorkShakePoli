from django import forms
from .models import Inicio

class inicioSesion(forms.ModelForm):
    class meta:
        model = Inicio
        fields = ['email','password']
        widgets = {
            'password': forms.PasswordInput(),  # Para que el campo de contraseña sea de tipo password
        } 
