from django.db import models

class Category(models.Model):
    """
    Categoría principal asociada a WordShake.
    """
    name = models.CharField("Nombre", max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class Level(models.Model):
    """
    Nivel dentro de una categoría.
    """
    name = models.CharField("Nombre Nivel", max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='levels',
        verbose_name="Categoría"
    )
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        unique_together = ('category', 'name')
        verbose_name = "Nivel"
        verbose_name_plural = "Niveles"
        ordering = ['category__name', 'order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"