# game/serializers.py
from rest_framework import serializers
from .models import Game, Submission

class GameCreateIn(serializers.Serializer):
    """
    Payload para crear partida (puedes ampliar luego).
    """
    lang = serializers.CharField(required=False, default="es")
    duration_seconds = serializers.IntegerField(
        required=False, min_value=30, max_value=3600, default=180
    )

class GameOut(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "board_seed", "status", "total_score", "created_at", "finished_at"]

class SubmitIn(serializers.Serializer):
    """
    Envío de palabra.
    """
    word = serializers.CharField(max_length=64)
    lang = serializers.CharField(required=False, default="es")
    idempotency_key = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class SubmitOut(serializers.Serializer):
    accepted = serializers.BooleanField()
    reason = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    delta = serializers.IntegerField()
    total = serializers.IntegerField()

class FinishOut(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "status", "total_score", "finished_at"]

__all__ = [
    "GameCreateIn",
    "GameOut",
    "SubmitIn",
    "SubmitOut",
    "FinishOut",
]
