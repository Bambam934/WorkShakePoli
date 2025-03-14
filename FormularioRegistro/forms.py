from django import forms
from .models import Registro
import re
from django.core.exceptions import ValidationError

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # Campo de contraseña

    class Meta:
        
        model = Registro
        fields = ['nombre', 'nombreUsuario','apellido', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Registro.objects.filter(email=email).exists():  # pylint: disable=no-member
            self.add_error("email", "Este correo electronico ya esta registrado")
        return email

    def clean_nombreUsuario(self):
        nombre = self.cleaned_data.get('nombreUsuario')
        if Registro.objects.filter(nombreUsuario=nombre).exists():  # pylint: disable=no-member
            self.add_error("email", "Este nombre de usuario ya esta en uso")
        return nombre

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 10:
            self.add_error("password","La contraseña debe tener al menos 10 caracteres.")
        if not any(char.islower() for char in password):
            self.add_error("password","La contraseña debe contener al menos una letra minúscula.")
        if not any(char.isupper() for char in password):
            self.add_error("password","La contraseña debe contener al menos una letra mayúscula.")
        if not any(char.isdigit() for char in password):
            self.add_error("password","La contraseña debe contener al menos un número.")
        if not re.search(r'[.,#\-*]', password):
            self.add_error("password","La contraseña debe contener al menos un carácter especial (.,#-).")
        return password
