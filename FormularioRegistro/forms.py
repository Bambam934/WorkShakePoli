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
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_nombreUsuario(self):
        nombre = self.cleaned_data.get('nombreUsuario')
        if Registro.objects.filter(nombreUsuario=nombre).exists():  # pylint: disable=no-member
            raise forms.ValidationError("Este nombre de usuario ya está registrado")
        return nombre

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:  # Allow shorter passwords for testing
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return password
