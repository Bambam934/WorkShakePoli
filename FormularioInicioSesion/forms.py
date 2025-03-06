from django import forms
from .models import Inicio

class inicioSesion(forms.ModelForm):
    class meta:
        model = Inicio
        fields = ['email','password']
        widgets = {
            'password': forms.PasswordInput(),  # Para que el campo de contraseña sea de tipo password
        }

    def emailRegistra(self):
        email = self.cleaned_data.get('email')
        if not(Inicio.objects.filter(email=email).exists()):
            raise forms.ValidationError("El correo electronico no esta registrado, si no tienes una cuenta puedes crear una ")
        else:
            verificacionPS(self)
        return email     
  
    