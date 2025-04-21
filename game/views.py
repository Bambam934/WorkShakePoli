# game/views.py
import json
from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required
from categorias.models import Level # Importa Level, ya no Category directamente aquí
from .models import Word
from .forms import WordForm
from . import services
# from django.http import JsonResponse # Importar si implementas validación AJAX

@login_required
def game_view(request, categoria_name, nivel_name):
    """
    Vista principal del juego para una categoría y nivel específicos.
    """
    error_message = None
    board_list = []
    valid_words_list = []
    level_obj = None

    try:
        # Busca el Nivel específico usando su nombre y el nombre de su categoría padre
        level_obj = Level.objects.select_related('category').get(
            name=nivel_name,
            category__name=categoria_name
        )
        # Obtiene las palabras asociadas directamente a este Level
        # Usamos el related_name 'words' definido en el M2M de Word.levels
        words_for_level = level_obj.words.all()

        if words_for_level.exists():
            board = services.generate_board_with_required_letters(words_for_level)
            valid_words_list = [word.text.upper() for word in words_for_level]
        else:
            error_message = f"Aún no hay palabras definidas para el nivel '{nivel_name}' en '{categoria_name}'."
            # Genera tablero aleatorio si no hay palabras específicas
            board = services.generate_board()

        # Asegura que board sea una lista para json.dumps
        if board is None: board_list = []
        elif isinstance(board, str): board_list = list(board)
        else: board_list = list(board or [])

    except Level.DoesNotExist:
        # Si el nivel/categoría no existe, muestra un error claro o un 404
        error_message = f"El nivel '{nivel_name}' en la categoría '{categoria_name}' no existe o no se pudo encontrar."
        # raise Http404("Nivel no encontrado.") # Alternativa: lanzar 404
        board_list = list(services.generate_board()) # Tablero aleatorio
    except Exception as e:
        # Captura otros errores
        error_message = "Ocurrió un error inesperado al cargar el juego."
        # logger.error(f"Error en game_view: {e}") # Loggear el error real
        board_list = []


    # Serializa a JSON los datos para JavaScript
    board_json = json.dumps(board_list)
    valid_words_json = json.dumps(valid_words_list)

    form = WordForm()

    # Renderiza la plantilla del juego con el contexto necesario
    return render(request, 'game/game.html', {
        'board_json': board_json,             # Para generar el tablero en JS
        'valid_words_json': valid_words_json, # Para validar palabras en JS
        'form': form,
        'categoria_name': categoria_name,     # Nombre de la categoría actual
        'nivel_name': nivel_name,             # Nombre del nivel actual
        'error_message': error_message,       # Mensaje de error si lo hubo
    })

# Considera añadir vistas AJAX aquí si quieres implementar validación
# de palabras en el servidor y guardado de puntaje sin recargar página.
# Ejemplo:
# @login_required
# def validate_word_ajax(request):
#     # ... lógica para recibir palabra, validar contra services.check_word_api
#     # y devolver JsonResponse({'valid': True/False, 'score': X}) ...
#     pass