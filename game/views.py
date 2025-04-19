from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import WordForm
from .models import Category
from . import services


def index(request):
    return HttpResponse("¡Bienvenido a WordShake!")
# game/views.py
from django.shortcuts import render
from .models import Category, Word

def select_level_view(request):
    subcategorias = Category.objects.filter(parent__isnull=True)

    niveles_por_categoria = {}
    for cat in subcategorias:
        niveles = Category.objects.filter(parent=cat).order_by('id')
        niveles_por_categoria[str(cat.id)] = [nivel.name.split()[-1] for nivel in niveles]

    return render(request, 'select_level.html', {
        'subcategorias': subcategorias,
        'niveles_por_categoria': niveles_por_categoria,
    })

def levels_view(request, categoria):
    try:
        categoria_obj = Category.objects.get(name=categoria, parent=None)
        niveles = categoria_obj.subcategories.all()
    except Category.DoesNotExist:
        niveles = []
    return render(request, 'levels.html', {'categoria': categoria, 'niveles': niveles})

def game_view(request, categoria_id, nivel):
    try:
        cat = Category.objects.get(name=categoria_id, parent=None) 
        nivel_obj = Category.objects.get(name=nivel, parent=cat)
        words = Word.objects.filter(categories=nivel_obj)
        board = services.generate_custom_game_board(categoria_id,nivel)
        valid_words = [word.text.upper() for word in words]
    # En game_view
    except Category.DoesNotExist:
        error = "Categoría o nivel no encontrado"
        board = services.generate_board()
        valid_words = []


    form = WordForm()
    return render(request, 'game.html', {
        'board': board,
        'form': form,
        'categoria': categoria_id,
        'nivel': nivel,
        'valid_words': valid_words, 
    })
