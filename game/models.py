from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey  
from django.core.exceptions import ValidationError

class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)
    points = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.word} ({self.points} pts)"

class Category(MPTTModel):
    name = models.CharField("Nombre", max_length=100, unique=True)
    parent = TreeForeignKey(
        'self',
        verbose_name="Categoría padre",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return str(self.name)  # ✅ Cambiado de 'text' a 'name'

class Word(models.Model):
    text = models.CharField("Palabra", max_length=50, unique=True)
    categories = models.ManyToManyField(Category, verbose_name="Categorías")
    is_from_api = models.BooleanField("De la API", default=False)
    is_validated = models.BooleanField(default=False)
    
    is_validated = models.BooleanField("¿Validada?", default=False)


    def clean(self):
        if not self.text.isalpha():
            raise ValidationError("Solo se permiten letras")
    
    class Meta:
        verbose_name = "Palabra"
        verbose_name_plural = "Palabras"

    def __str__(self):
        return str(self.text)