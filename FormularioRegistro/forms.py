from django import forms
from .models import Registro
import re
from django.core.exceptions import ValidationError

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['nombre', 'apellido', 'email', 'telefono', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Para que el campo de contraseña sea de tipo password
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Registro.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email



    #Funcion para las restricciones de la contraseña    

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 10:
            raise ValidationError("La contraseña debe tener al menos 10 caracteres.")
        if not any(char.islower() for char in password):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not any(char.isupper() for char in password):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[.,#-]', password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial (.,#-).")
        return password

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{10}$', telefono):  # Ejemplo: 10 dígitos
            raise forms.ValidationError("El teléfono debe tener 10 dígitos.")
        return telefono