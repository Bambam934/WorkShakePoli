# categorias/admin.py
from django.contrib import admin
from .models import Game, Category, Level

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('game', 'name')
    list_filter = ('game',)
    search_fields = ('name',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'order')
    list_filter = ('category__game', 'category')
    search_fields = ('name',)
    ordering = ('category__game__name', 'category__name', 'order')