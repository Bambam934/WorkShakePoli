# game/views.py
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from categorias.models import Level
from perfil.models     import UserProfile          # perfil.UserProfile
from . import services

@login_required
def game_view(request, categoria_name, nivel_name):
    error_message      = None
    board_list         = []
    valid_words_list   = []

    # ─── Color neón del perfil ───────────────────────────
    user_neon_color = '#00ffcc'
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_neon_color = profile.neon_color or user_neon_color

    # ─── Skin activa ─────────────────────────────────────
    active_skin = profile.active_skin.slug if profile.active_skin else None

    # ─── Lógica de nivel / tablero ───────────────────────
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
            error_message = f"Aún no hay palabras para «{nivel_name}»."
            board = services.generate_board()

        board_list = list(board)

    except Level.DoesNotExist:
        error_message = (
            f"El nivel «{nivel_name}» en la categoría «{categoria_name}» no existe."
        )
        board_list = list(services.generate_board())

    except Exception as e:
        error_message = "Ocurrió un error al cargar el juego."
        print("Error en game_view:", e)
        board_list = list(services.generate_board())

    context = {
        "board_json":       json.dumps(board_list),
        "valid_words_json": json.dumps(valid_words_list),
        "categoria_name":   categoria_name,
        "nivel_name":       nivel_name,
        "error_message":    error_message,
        "niveles":          Level.objects.filter(category__name=categoria_name),
        "neon_color":       user_neon_color,
        "active_skin":      active_skin,        # ← clave nueva
    }
    return render(request, "game/game.html", context)
