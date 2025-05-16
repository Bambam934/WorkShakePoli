# achievements/services.py
from django.utils import timezone
from asgiref.sync    import async_to_sync
from channels.layers import get_channel_layer

from .models import (
    Achievement, UserAchievement,
    Challenge,   UserChallengeProgress,
    Skin,
)

# ────────────────────────────────────────────────────────────────────
# 1)  NOTIFICACIÓN WEBSOCKET
# ────────────────────────────────────────────────────────────────────
def notify_achievement(user, achievement):
    """
    Envía un mensaje por WebSocket al grupo «user_<id>»
    para que el navegador muestre el toast.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",                      # grupo → NotificationConsumer
        {
            "type": "achievement_unlocked",     # ← debe coincidir con el handler
            "data": {
                "name":        achievement.name,
                "description": achievement.description,
            },
        },
    )


# ────────────────────────────────────────────────────────────────────
# 2)  LOGROS: comprobar y otorgar
# ────────────────────────────────────────────────────────────────────
def check_achievements(user, metric_name, new_total):
    """
    Comprueba todos los logros cuyo «trigger_type» coincide
    y el valor objetivo (target_value) ≤ new_total.
    Crea UserAchievement si procede y envía la notificación.
    """
    qs = Achievement.objects.filter(
        trigger_type=metric_name,
        target_value__lte=new_total,
    )

    for ach in qs:
        ua, created = UserAchievement.objects.get_or_create(
            user=user,
            achievement=ach,
        )
        if created:
            # ▶ notificación en tiempo real
            notify_achievement(user, ach)

            # ejemplo de recompensa: regalar una skin
            if ach.slug == "first-500":
                profile = user.userprofile
                profile.owned_skins.add(
                    Skin.objects.get(slug="neon-blue")
                )


# ────────────────────────────────────────────────────────────────────
# 3)  DESAFÍOS: progreso y completado
# ────────────────────────────────────────────────────────────────────
def update_challenge_progress(user, metric_name, increment=1):
    """
    Suma `increment` al progreso del desafío activo cuyo
    metric coincide (daily_score, level_completed, etc.).
    Marca `completed` si alcanza el target.
    """
    now = timezone.now()
    active = Challenge.objects.filter(
        metric=metric_name,
        start__lte=now,
        end__gte=now,
    )

    for ch in active:
        prog, _ = UserChallengeProgress.objects.get_or_create(
            user=user,
            challenge=ch,
        )
        if prog.completed:
            continue

        prog.progress += increment
        if prog.progress >= ch.target_value:
            prog.completed = True
        prog.save()
