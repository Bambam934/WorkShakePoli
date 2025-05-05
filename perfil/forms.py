from django import forms
from .models import UserProfile
from django.db import models

from django.core.exceptions import ValidationError

def validar_tamano_imagen(imagen):
    limite = 2.5 * 1024 * 1024  # 2.5 MB
    if imagen.size > limite:
        raise ValidationError('La imagen excede el tamaño máximo de 2.5MB.')

class Perfil(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', validators=[validar_tamano_imagen])

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }