# categorias/admin.py
from django.contrib import admin
from .models import Category, Level # Importa los modelos actualizados

# Inline para gestionar niveles desde la vista de Categoría
class LevelInline(admin.TabularInline):
    model = Level
    extra = 1 # Número de formularios extra para añadir niveles
    fields = ('name', 'order') # Campos a mostrar en el inline
    ordering = ('order', 'name') # Orden dentro del inline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): # Hereda de ModelAdmin normal
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [LevelInline] # Añade el inline para gestionar niveles aquí

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order') # Muestra nombre, categoría y orden
    list_filter = ('category',) # Permite filtrar por categoría
    search_fields = ('name', 'category__name') # Busca por nombre de nivel o categoría
    list_editable = ('order',) # Permite editar el orden directamente en la lista
    ordering = ('category__name', 'order', 'name') # Orden por defecto de la lista
    # Opcional: autocompletar categoría si tienes muchas
    # autocomplete_fields = ['category']