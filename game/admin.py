# game/admin.py
from django.contrib import admin, messages
from .models import Word
from categorias.models import Level
import requests

def validar_palabra(palabra):
    # Implementa tu lógica o API externa…
    return True

def importar_palabras_desde_datamuse(modeladmin, request, queryset):
    # Lógica para importar…
    pass


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_from_api', 'es_valida')
    search_fields = ('text',)
    filter_horizontal = ('levels',)  # Many-to-Many con Level
    actions = [importar_palabras_desde_datamuse]

    def es_valida(self, obj):
        return validar_palabra(obj.text)
    es_valida.boolean = True
    es_valida.short_description = 'Válida (API)'
