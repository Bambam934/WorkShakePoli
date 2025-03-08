from django import forms
from FormularioRegistro import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import render

class InicioSesionForm(forms.ModelForm):
    class Meta:
        model = models.Registro
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not(models.Registro.objects.filter(email=email).exists()):
            self.add_error('email', 'Este correo electrónico no está registrado. Puedes crearte una cuenta')
        else:
            self.errors.pop('email', None)
        return email
    
    

    