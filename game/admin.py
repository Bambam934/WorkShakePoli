# game/admin.py
from django.contrib import admin
from django.contrib import messages
from .models import Word
import requests

# Las funciones validar_palabra y importar_palabras_desde_datamuse
# pueden permanecer aquí o moverse a un archivo utils.py si prefieres.

def validar_palabra(palabra):
    # ... (código sin cambios) ...
    pass

def importar_palabras_desde_datamuse(modeladmin, request, queryset):
    # ... (código sin cambios, asegura que guarde en mayúsculas si es necesario) ...
    pass

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_from_api', 'es_valida')
    search_fields = ('text',)
    # CAMBIO: Apunta al nuevo campo ManyToMany 'levels'
    filter_horizontal = ('levels',)
    actions = [importar_palabras_desde_datamuse]

    def es_valida(self, obj):
        # Reusa la función helper
        return validar_palabra(obj.text)
    es_valida.boolean = True
    es_valida.short_description = 'Válida (API)' # Cambiado para claridad

    # Opcional: Añadir un campo para ver los niveles en la lista
    # def display_levels(self, obj):
    #    return ", ".join([level.name for level in obj.levels.all()])
    # display_levels.short_description = 'Niveles'
    # list_display = ('text', 'is_from_api', 'es_valida', 'display_levels')