# achievements/services.py
from django.utils import timezone
from .models import Achievement, UserAchievement, Challenge, UserChallengeProgress
from asgiref.sync    import async_to_sync
from channels.layers import get_channel_layer

from .models import Achievement, UserAchievement, Skin

def check_achievements(user, metric_name, new_total):
    """Evalúa si el usuario desbloquea algo según el métrico actualizado."""
    qs = Achievement.objects.filter(trigger_type=metric_name, target_value__lte=new_total)
    for ach in qs:
        UserAchievement.objects.get_or_create(user=user, achievement=ach)

def update_challenge_progress(user, metric_name, increment=1):
    now = timezone.now()
    active = Challenge.objects.filter(metric=metric_name, start__lte=now, end__gte=now)
    for ch in active:
        prog, _ = UserChallengeProgress.objects.get_or_create(user=user, challenge=ch)
        if not prog.completed:
            prog.progress += increment
            if prog.progress >= ch.target_value:
                prog.completed = True
            prog.save()


def notify_achievement(user, achievement):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"user_{user.id}",
        {
            "type": "achievement.unlocked",
            "data": {
                "name": achievement.name,
                "description": achievement.description
            }
        }
    )
    
def check_achievements(user, metric_name, new_total):
    qs = Achievement.objects.filter(
        trigger_type=metric_name,
        target_value__lte=new_total
    )
    for ach in qs:
        ua, created = UserAchievement.objects.get_or_create(
            user=user, achievement=ach
        )
        if created:
            # notificación por WebSocket
            notify_achievement(user, ach)

            # → aquí regalamos la skin por ese logro concreto
            if ach.slug == 'first-500':
                profile = user.userprofile
                profile.owned_skins.add(
                    Skin.objects.get(slug='neon-blue')
                )