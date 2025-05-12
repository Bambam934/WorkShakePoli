# game/views.py
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from categorias.models import Level
# Asegúrate que la importación de UserProfile sea correcta
from perfil.models import UserProfile # Ajusta 'perfil' si el nombre de tu app es otro
from . import services

@login_required
def game_view(request, categoria_name, nivel_name):
    error_message = None
    board_list: list[str] = []
    valid_words_list: list[str] = []
    
    # Valor por defecto inicial, por si algo falla
    user_neon_color = '#00ffcc' 

    if request.user.is_authenticated:
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            if profile.neon_color: 
                user_neon_color = profile.neon_color
                print(user_neon_color)
            else:
                user_neon_color = UserProfile._meta.get_field('neon_color').default

        except UserProfile.DoesNotExist:
            user_neon_color = UserProfile._meta.get_field('neon_color').default
        except Exception as e:
            try:
                user_neon_color = UserProfile._meta.get_field('neon_color').default
            except Exception as e_default:
                user_neon_color = '#00ffcc' # Último recurso
    
    # ... (resto de tu lógica para cargar el juego: level_obj, words_for_level, etc.)
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
    except Exception as e:
        error_message = "Ocurrió un error al cargar la información del juego."
        print(f"Error en lógica de juego (game_view): {e}")
        board_list = list(services.generate_board()) # Fallback seguro


    context = {
        "board_json":       json.dumps(board_list),
        "valid_words_json": json.dumps(valid_words_list),
        "categoria_name":   categoria_name,
        "nivel_name":       nivel_name,
        "error_message":    error_message,
        "niveles":          Level.objects.filter(category__name=categoria_name),
        "neon_color":       user_neon_color, # Esta es la clave que usa tu game.html
    }
    return render(request, "game/game.html", context)

def achievements(request):
    return render(request, 'game/achievements.html')


