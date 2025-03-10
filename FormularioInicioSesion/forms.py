from django import forms
from django.contrib.auth import authenticate
from FormularioRegistro import models

class InicioSesionForm(forms.Form):  # ❌ No debe ser ModelForm
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            self.add_error("email", "Debe ingresar un correo.")
            self.add_error("password", "Debe ingresar una contraseña.")
            return cleaned_data

        # Usar authenticate en lugar de check_password
        user = authenticate(username=email, password=password)

        if user is None:
            self.add_error("email", "Correo o contraseña incorrectos.")
            return cleaned_data

        return cleaned_data
