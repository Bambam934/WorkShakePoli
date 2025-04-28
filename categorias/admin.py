# categorias/admin.py
from django.contrib import admin
from .models import Category, Level

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category__name', 'order')
