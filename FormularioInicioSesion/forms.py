import email
from django import forms
from FormularioRegistro import models
from django.contrib.auth.hashers import check_password
from django import forms
from django.contrib.auth.hashers import check_password



class InicioSesionForm(forms.ModelForm):
    class Meta:
        model = models.Registro
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            self.add_error("email", "Debe ingresar un correo.")
            self.add_error("password", "Debe ingresar una contraseña.")
            return cleaned_data

        # Buscar el usuario en la base de datos
        usuario = models.Registro.objects.filter(email=email).first()

        if usuario is None:
            self.add_error("email", "Correo no registrado. Puedes crearte una cuenta.")
            return cleaned_data

        # Comparar la contraseña ingresada con la almacenada en la BD
        if not check_password(password, usuario.password):
            self.add_error("password", "Contraseña incorrecta.")
            return cleaned_data

        return cleaned_data

    