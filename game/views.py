# game/views.py
import json
from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required
from categorias.models import Level, Category  # Añadir Category si es necesario
from .models import Word
from .forms import WordForm
from . import services

@login_required
def game_view(request, categoria_name, nivel_name):
    """
    Vista unificada del juego usando nombres de categoría y nivel
    """
    error_message = None
    board_list = []
    valid_words_list = []
    level_obj = None

    try:
        # Usamos el modelo Level para obtener el nivel específico
        level_obj = Level.objects.select_related('category').get(
            name=nivel_name,
            category__name=categoria_name
        )
        words_for_level = level_obj.words.all()

        if words_for_level.exists():
            board = services.generate_board_with_required_letters(words_for_level)
            valid_words_list = [word.text.upper() for word in words_for_level]
        else:
            error_message = f"Aún no hay palabras definidas para el nivel '{nivel_name}' en '{categoria_name}'."
            board = services.generate_board()

        # Conversión segura a lista
        board_list = list(board) if not isinstance(board, list) else board
        valid_words_json = json.dumps(valid_words_list)
        board_json = json.dumps(board_list)

    except Level.DoesNotExist:
        error_message = f"El nivel '{nivel_name}' en la categoría '{categoria_name}' no existe."
        board_json = json.dumps(list(services.generate_board()))
        valid_words_json = json.dumps([])

    except Exception as e:
        error_message = "Error inesperado al cargar el juego."
        board_json = json.dumps([])
        valid_words_json = json.dumps([])

    form = WordForm()

    return render(request, 'game/game.html', {
        'board_json': board_json,
        'valid_words_json': valid_words_json,
        'form': form,
        'categoria_name': categoria_name,
        'nivel_name': nivel_name,
        'error_message': error_message
    })