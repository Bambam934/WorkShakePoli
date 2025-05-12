
# achievements/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import UserChallengeProgress

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
