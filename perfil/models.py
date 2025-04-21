from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # Otros campos que puedas necesitar para el perfil

    def __str__(self):
        return self.user.email  # O self.user.nombreUsuario, dependiendo de cómo quieras identificar al usuario