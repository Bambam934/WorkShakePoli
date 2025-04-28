# game/views.py
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from categorias.models import Level
from . import services


@login_required
def game_view(request, categoria_name, nivel_name):
    """Carga el tablero y las palabras válidas para el nivel elegido."""
    error_message = None
    board_list: list[str] = []
    valid_words_list: list[str] = []

    try:
        level_obj = (
            Level.objects
            .select_related('category')
            .get(name=nivel_name, category__name=categoria_name)
        )
        words_for_level = level_obj.words.all()

        if words_for_level.exists():
            board = services.generate_board_with_required_letters(words_for_level)
            valid_words_list = [w.text.upper() for w in words_for_level]
        else:
            error_message = (
                f"Aún no hay palabras para «{nivel_name}» en «{categoria_name}»."
            )
            board = services.generate_board()

        board_list = list(board)

    except Level.DoesNotExist:
        error_message = (
            f"El nivel «{nivel_name}» en la categoría «{categoria_name}» no existe."
        )
        board_list = list(services.generate_board())

    return render(
        request,
        "game.html",
        {
            "board_json":       json.dumps(board_list),        # ← 25 letras
            "valid_words_json": json.dumps(valid_words_list),  # ← diccionario
            "categoria_name":   categoria_name,
            "nivel_name":       nivel_name,
            "error_message":    error_message,
            "niveles":          Level.objects.filter(category__name=categoria_name),
        },
    )
