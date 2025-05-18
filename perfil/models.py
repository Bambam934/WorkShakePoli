# perfil/models.py
from django.db import models
from django.conf import settings
from achievements.models import Skin

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    neon_color = models.CharField(
        max_length=20,
        default='#00ffcc'
    )

    # 🔸 Logros desbloqueados (nunca NULL)
    achievements = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de IDs de logros obtenidos"
    )

    # 🔸 Puntos totales (nunca NULL)
    puntos = models.PositiveIntegerField(
        default=0,
        help_text="Puntos acumulados por el usuario"
    )

    # 🔸 Nuevos contadores 🔸
    total_score = models.PositiveIntegerField(default=0)
    total_words = models.PositiveIntegerField(default=0)
    coins       = models.PositiveIntegerField(default=0)

    # ✨ Skins 🔸
    owned_skins = models.ManyToManyField(
        Skin,
        blank=True,
        related_name='owners'
    )
    active_skin = models.ForeignKey(
        Skin,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.user.email
