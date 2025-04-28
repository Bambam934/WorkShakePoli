# categorias/admin.py
from django.contrib import admin
from .models import Category, Level # Importa los modelos aquí

# --- PEGA LevelInline AQUÍ ---
# Inline para gestionar niveles desde la vista de Categoría
class LevelInline(admin.TabularInline):
    model = Level # 'Level' sí está definido aquí porque lo importaste arriba
    extra = 1
    fields = ('name', 'order')
    ordering = ('order', 'name')
# --- FIN de LevelInline ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [LevelInline] # Ahora puede encontrar LevelInline

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    list_editable = ('order',)
    ordering = ('category__name', 'order', 'name')