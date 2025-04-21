# categorias/models.py
from django.db import models

# Modelo simplificado para Categorías Principales
class Category(models.Model):
    name = models.CharField("Nombre", max_length=100, unique=True)

    class Meta:
        # Puedes quitar db_table si quieres que la tabla se llame 'categorias_category'
        # Si la tabla 'categorias_category' ya existe y tiene datos de categorías
        # principales que quieres conservar, mantenla. Si no, quítala.
        # db_table = "categorias_category"
        verbose_name = "Categoría Principal"
        verbose_name_plural = "Categorías Principales"
        ordering = ['name'] # Ordenar por nombre

    def __str__(self):
        return str(self.name)

# Nuevo modelo para Niveles
class Level(models.Model):
    name = models.CharField("Nombre Nivel", max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE, # Borrar niveles si se borra la categoría
        related_name='levels',    # Cómo acceder a niveles desde Category (category.levels.all())
        verbose_name="Categoría Principal"
    )
    # Campo opcional para ordenar niveles
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        # Nombre de nivel único DENTRO de su categoría
        unique_together = ('category', 'name')
        # Orden por defecto: por categoría, luego por orden, luego por nombre
        ordering = ['category__name', 'order', 'name']
        verbose_name = "Nivel"
        verbose_name_plural = "Niveles"
        # La tabla por defecto será 'categorias_level'

    def __str__(self):
        return f"{self.category.name} - {self.name}"