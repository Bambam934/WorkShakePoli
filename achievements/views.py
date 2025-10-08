
# achievements/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import UserChallengeProgress
from django.http                import HttpResponse
from django.contrib.auth.decorators import login_required
from asgiref.sync               import async_to_sync
from channels.layers            import get_channel_layer
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from game.models import Game

@login_required
def claim_reward(request, progress_id):
    prog = get_object_or_404(
        UserChallengeProgress,
        id=progress_id,
        user=request.user,
        completed=True,
        claimed=False
    )
    # …otorga recompensa…
    prog.claimed = True
    prog.save()
    messages.success(request, "¡Recompensa reclamada!")
    return redirect('perfil:detalle')   # o la URL que tengas

@login_required
def debug_send(request):
    """
    Envía un evento ‘achievement_unlocked’ al usuario logeado.
    URL temporal sólo para pruebas.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{request.user.id}",              # grupo de ese usuario
        {
            "type": "achievement_unlocked",     # ← handler del consumer
            "data": {
                "name":  "Logro de prueba",
                "description": "Enviado desde /debug-send/",
            },
        }
    )
    return HttpResponse("Mensaje enviado ✔")

class LeaderboardView(APIView):
    """
    GET /achievements/api/v1/leaderboards?scope=daily|weekly|all
    Devuelve top usuarios por puntaje total (sumatoria de total_score en juegos finalizados).
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        scope = request.GET.get("scope", "daily")
        qs = Game.objects.filter(status=Game.Status.FINISHED)

        now = timezone.now()
        if scope == "daily":
            qs = qs.filter(created_at__gte=now - timedelta(days=1))
        elif scope == "weekly":
            qs = qs.filter(created_at__gte=now - timedelta(days=7))
        # else: "all" => sin filtro de tiempo

        # Agrega por usuario
        agg = (
            qs.values("player__id", "player__email")
              .annotate(total=Sum("total_score"))
              .order_by("-total")[:50]
        )

        items = [
            {
                "user_id": row["player__id"],
                "email": row["player__email"],
                "total": row["total"] or 0,
            }
            for row in agg
        ]
        return Response({"scope": scope, "items": items})