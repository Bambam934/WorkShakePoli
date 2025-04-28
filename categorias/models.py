from django.db import models

# Juego de Wordshake\ n# (Tabla temporalmente creada con FK null para migraciones)
class Game(models.Model):
    name = models.CharField("Juego", max_length=100, unique=True)

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Categoría asociada a un Juego de Wordshake.
    """
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Juego",
        null=True,
        blank=True  # Permite NULL temporalmente para migraciones
    )
    name = models.CharField("Nombre Categoría", max_length=100)

    class Meta:
        unique_together = ('game', 'name')
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['game__name', 'name']

    def __str__(self):
        return f"{self.game.name if self.game else 'sin juego'} - {self.name}"


class Level(models.Model):
    """
    Nivel dentro de una Categoría.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='levels',
        verbose_name="Categoría"
    )
    name = models.CharField("Nombre Nivel", max_length=100)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        unique_together = ('category', 'name')
        verbose_name = "Nivel"
        verbose_name_plural = "Niveles"
        ordering = ['category__game__name', 'category__name', 'order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"