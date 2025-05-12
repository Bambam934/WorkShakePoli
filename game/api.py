# game/api.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt    # si NO usas cookie csrf
from django.contrib.auth.decorators import login_required
from achievements.services import (
    check_achievements, update_challenge_progress
)

@login_required
@require_POST
def registrar_partida(request):
    data = json.loads(request.body)
    puntos = int(data.get('score', 0))
    palabras = int(data.get('words', 0))

    perfil = request.user

    # Estadísticas acumuladas (asegúrate de tener estos campos)
    perfil.total_score = getattr(perfil, 'total_score', 0) + puntos
    perfil.total_words = getattr(perfil, 'total_words', 0) + palabras
    perfil.save()

    # Logros permanentes
    check_achievements(perfil, 'score',  perfil.total_score)
    check_achievements(perfil, 'words',  perfil.total_words)

    # Desafíos temporales
    update_challenge_progress(perfil, 'daily_score', puntos)
    update_challenge_progress(perfil, 'level_completed', 1)

    return JsonResponse({'ok': True})
