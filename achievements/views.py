
# achievements/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import UserChallengeProgress
from django.http                import HttpResponse
from django.contrib.auth.decorators import login_required
from asgiref.sync               import async_to_sync
from channels.layers            import get_channel_layer

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