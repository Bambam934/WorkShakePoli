# game/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)
    points = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.word} ({self.points} pts)"

class Word(models.Model):
    text = models.CharField("Palabra", max_length=50, unique=True)
    levels = models.ManyToManyField(
        'categorias.Level',
        verbose_name="Niveles",
        related_name="words",
        blank=True
    )
    is_from_api = models.BooleanField("De la API", default=False)
    is_validated = models.BooleanField("¿Validada?", default=False)

    def clean(self):
        self.text = self.text.upper()
        if not self.text.isalpha():
            raise ValidationError("Solo se permiten letras")

    def save(self, *args, **kwargs):
        self.text = self.text.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Palabra"
        verbose_name_plural = "Palabras"
        ordering = ['text']

    def __str__(self):
        return str(self.text)

# ───────────────────────────────────────────────────────────────────
# ÚNICO modelo Game (fusionado)
# ───────────────────────────────────────────────────────────────────
class Game(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        RUNNING = "RUNNING", "Running"
        FINISHED = "FINISHED", "Finished"

    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="games",
    )
    board_seed = models.CharField(max_length=64, blank=True, default="")
    total_score = models.IntegerField(default=0)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["player"]),
        ]

    def is_active(self) -> bool:
        return (
            self.status == self.Status.RUNNING
            and (self.ends_at is None or self.ends_at >= timezone.now())
        )

    def __str__(self):
        return f"Game #{self.id} - {self.player} - {self.status}"

class Submission(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="submissions")
    word = models.CharField(max_length=64)
    lang = models.CharField(max_length=8, default="es")
    accepted = models.BooleanField(default=False)
    delta = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["game", "word"])]
        constraints = [
            # única solo si accepted=True
            models.UniqueConstraint(
                fields=["game", "word"],
                condition=Q(accepted=True),
                name="uniq_word_per_game_accepted",
            ),
        ]