# categorias/views.py
import json # Importa json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Para mensajes de error opcionales
from .models import Category, Level

@login_required
def select_level_view(request):
    """
    Muestra categorías y permite seleccionar nivel.
    Prepara datos para el dropdown dinámico de niveles.
    """
    categories = Category.objects.order_by('name')
    # Diccionario para pasar al JS: Clave=Nombre Categoría, Valor=Lista Nombres Nivel
    levels_by_category_name = {}
    # Usamos prefetch_related para optimizar la consulta de niveles
    for cat in Category.objects.prefetch_related('levels'):
        levels_by_category_name[cat.name] = [
            lvl.name for lvl in sorted(list(cat.levels.all()), key=lambda x: (x.order, x.name))
        ]

    # Pasamos las categorías para el primer select
    # y el diccionario mapeado para el JS (usando json_script en la plantilla)
    return render(request, 'select_level.html', {
        'categories': categories,
        'levels_by_category': levels_by_category_name,
    })


@login_required
def start_game_view(request):
    """
    Recibe la categoría y nivel seleccionados, valida, y redirige
    a la vista del juego en la app 'game'.
    """
    categoria_name = request.GET.get('categoria_name')
    nivel_name = request.GET.get('nivel')

    if not categoria_name or not nivel_name:
        messages.error(request, 'Debes seleccionar una categoría y un nivel.')
        return redirect('categorias:select_level')

    try:
        # Verifica que la categoría exista
        cat = Category.objects.get(name=categoria_name)
        # Verifica que el nivel exista Y pertenezca a esa categoría
        Level.objects.get(name=nivel_name, category=cat)
    except (Category.DoesNotExist, Level.DoesNotExist):
         messages.error(request, f'La categoría "{categoria_name}" o el nivel "{nivel_name}" no son válidos.')
         return redirect('categorias:select_level')

    # Redirige a la URL del juego ('game:play') pasando los nombres
    return redirect('game:play', categoria_name=categoria_name, nivel_name=nivel_name)