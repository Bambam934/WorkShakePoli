# game/views.py
import json
from collections import Counter
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework import status, permissions, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from categorias.models import Level
from perfil.models import UserProfile
from . import services
from .models import Game, Submission, Word
from .serializers import GameOut, SubmitIn


# ──────────────────────────────
# HTML del juego
# ──────────────────────────────
@login_required
def game_view(request, categoria_name, nivel_name):
    error_message    = None
    board_list       = []
    valid_words_list = []

    # Color neón del perfil / skin activa
    user_neon_color = '#00ffcc'
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_neon_color = profile.neon_color or user_neon_color
    active_skin = profile.active_skin.slug if profile.active_skin else None

    # Lógica de nivel / tablero
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
        error_message = f"El nivel «{nivel_name}» en la categoría «{categoria_name}» no existe."
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
        "active_skin":      active_skin,
    }
    return render(request, "game/game.html", context)


# ──────────────────────────────
# Helpers de validación / puntaje
# ──────────────────────────────
def _score_word(word: str) -> int:
    return sum(services.LETTER_POINTS.get(ch, 0) for ch in word.upper())

def _can_build_from_board(word: str, board_seed: str) -> bool:
    w = Counter(word.upper())
    b = Counter(board_seed.upper())
    return all(w[ch] <= b.get(ch, 0) for ch in w)


# ──────────────────────────────
# API: crear / enviar palabra / terminar / cancelar / obtener / listar
# ──────────────────────────────
class CreateGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # evita múltiples RUNNING simultáneas
        if Game.objects.filter(player=request.user, status=Game.Status.RUNNING).exists():
            return Response(
                {"detail": "You already have a running game"},
                status=status.HTTP_409_CONFLICT,
            )

        # semilla por request o generada
        board_seed = request.data.get("board_seed")
        if not board_seed:
            # si quieres tablero por categoría/nivel, descomenta y usa tu services personalizado:
            # categoria = request.data.get("category")
            # nivel     = request.data.get("level")
            # if categoria and nivel:
            #     board_seed = services.generate_custom_game_board(categoria, nivel)
            # else:
            board_seed = services.generate_board()

        g = Game.objects.create(
            player=request.user,
            board_seed=board_seed,
            status=Game.Status.RUNNING,
            # si manejas duración: ends_at=timezone.now() + timedelta(minutes=3),
        )
        return Response(GameOut(g).data, status=status.HTTP_201_CREATED)


class SubmitWordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, game_id: int):
        game = get_object_or_404(Game, pk=game_id, player=request.user)

        if game.status == Game.Status.FINISHED:
            return Response(
                {"accepted": False, "reason": "already_finished", "delta": 0, "total": game.total_score},
                status=400
            )

        s_in = SubmitIn(data=request.data)
        s_in.is_valid(raise_exception=True)
        word = s_in.validated_data["word"].upper()
        lang = s_in.validated_data["lang"]

        # no repetir palabras ya aceptadas
        if Submission.objects.filter(game=game, word=word, accepted=True).exists():
            return Response({"accepted": False, "reason": "duplicate", "delta": 0, "total": game.total_score})

        # validar contra tablero
        if not _can_build_from_board(word, game.board_seed):
            return Response({"accepted": False, "reason": "not_on_board", "delta": 0, "total": game.total_score})

        # validar diccionario local
        if not Word.objects.filter(text=word).exists():
            return Response({"accepted": False, "reason": "unknown_word", "delta": 0, "total": game.total_score})

        # puntuar + registrar
        delta = _score_word(word)
        Submission.objects.create(game=game, word=word, lang=lang, accepted=True, delta=delta)
        game.total_score = (game.total_score or 0) + delta
        game.save(update_fields=["total_score"])

        return Response({"accepted": True, "reason": None, "delta": delta, "total": game.total_score}, status=200)


class FinishGameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, game_id: int):
        game = get_object_or_404(Game, pk=game_id, player=request.user)

        if game.status == Game.Status.FINISHED:
            return Response({"detail": "Game already finished"}, status=400)

        game.status = Game.Status.FINISHED
        game.finished_at = timezone.now()
        game.save(update_fields=["status", "finished_at"])

        return Response(GameOut(game).data, status=200)


class CancelGameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, game_id: int):
        game = get_object_or_404(Game, pk=game_id, player=request.user)
        if game.status != Game.Status.RUNNING:
            return Response({"detail": "Game not running"}, status=400)

        game.status = Game.Status.FINISHED
        game.finished_at = timezone.now()
        game.save(update_fields=["status", "finished_at"])

        return Response(GameOut(game).data, status=200)


class GetGameView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameOut
    lookup_url_kwarg = "game_id"

    def get_queryset(self):
        return Game.objects.filter(player=self.request.user)


class ListMyGamesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameOut

    def get_queryset(self):
        return Game.objects.filter(player=self.request.user).order_by("-created_at")[:50]
