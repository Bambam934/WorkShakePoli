# categorias/admin.py
from django.contrib import admin
from .models import Category, Level

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)          # <-- sin 'parent'
    search_fields = ('name',)
    # list_filter = ('parent',)       # <-- quítalo si lo tenías

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category__name', 'order')
