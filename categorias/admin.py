# categorias/admin.py
from django.contrib import admin
# Quita MPTTModelAdmin
from .models import Category, Level # Importa ambos modelos
# Quita la importación de Word y WordInline si no se usan aquí

# Inline para mostrar/añadir niveles directamente en la página de Categoría
class LevelInline(admin.TabularInline):
    model = Level
    extra = 1
    ordering = ('order', 'name') # Ordena los inlines

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): # Usa admin.ModelAdmin normal
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [LevelInline] # Añade el inline para niveles

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')
    list_filter = ('category',) # Filtra por categoría
    search_fields = ('name', 'category__name')
    list_editable = ('order',) # Permite editar el orden en la lista
    ordering = ('category__name', 'order', 'name')