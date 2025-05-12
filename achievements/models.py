# achievements/models.py
from django.db import models
from django.conf import settings

class Achievement(models.Model):
    """Logro permanente, desbloqueable una sola vez."""
    slug         = models.SlugField(unique=True)
    name         = models.CharField(max_length=60)
    description  = models.TextField()
    icon         = models.ImageField(upload_to='achievements/icons/')
    # lógica para desbloquear
    trigger_type = models.CharField(max_length=30, choices=[
        ('score', 'Puntaje total'),          # ej. superar X puntos históricos
        ('words', 'Palabras encontradas'),   # …
        ('streak', 'Rachas diarias'),        # …
    ])
    target_value = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Relación M‑M entre usuario y logro, con fecha."""
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement  = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')


class Challenge(models.Model):
    """Desafío temporal (diario, semanal)."""
    slug          = models.SlugField(unique=True)
    name          = models.CharField(max_length=80)
    description   = models.TextField()
    icon          = models.ImageField(upload_to='challenges/icons/', blank=True)
    start         = models.DateTimeField()
    end           = models.DateTimeField()
    target_value  = models.PositiveIntegerField()
    metric        = models.CharField(max_length=30, choices=[
        ('daily_score', 'Puntaje diario'),
        ('level_completed', 'Niveles completados'),
        # añade los que necesites
    ])

    def __str__(self):
        return self.name


class UserChallengeProgress(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    progress  = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    claimed   = models.BooleanField(default=False)  # si ya tomó la recompensa

    class Meta:
        unique_together = ('user', 'challenge')


class Skin(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='skins/icons/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name