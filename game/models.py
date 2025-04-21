# game/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
# Ya no necesitamos importar Category o Level aquí directamente

class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)
    points = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.word} ({self.points} pts)"

class Word(models.Model):
    text = models.CharField("Palabra", max_length=50, unique=True)
    # CAMBIO: Apunta al modelo Level de la app categorias
    levels = models.ManyToManyField(
        'categorias.Level',  # Apunta al nuevo modelo Level
        verbose_name="Niveles",
        related_name="words", # Cómo acceder a palabras desde Level (level.words.all())
        blank=True           # Permite que una palabra no esté en ningún nivel
    )
    is_from_api = models.BooleanField("De la API", default=False)
    is_validated = models.BooleanField("¿Validada?", default=False)

    def clean(self):
        # Convierte a mayúsculas antes de validar para asegurar consistencia
        self.text = self.text.upper()
        if not self.text.isalpha():
            raise ValidationError("Solo se permiten letras")

    # Opcional: Sobrescribir save para asegurar mayúsculas
    def save(self, *args, **kwargs):
        self.text = self.text.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Palabra"
        verbose_name_plural = "Palabras"
        ordering = ['text'] # Ordenar por texto

    def __str__(self):
        return str(self.text)