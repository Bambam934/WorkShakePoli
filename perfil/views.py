# perfil/views.py

from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http                    import JsonResponse
from django.views.decorators.csrf   import csrf_exempt
from django.contrib                 import messages
from django.db                      import transaction
from django.utils                   import timezone

from .forms                         import ProfilePictureForm
from .models                        import UserProfile
from achievements.models            import (
    Achievement, UserAchievement,
    Challenge,  UserChallengeProgress,
    Skin                     # ← Import correcto
)


@csrf_exempt
def update_neon_color(request):
    if request.method == 'POST' and request.user.is_authenticated:
        color = request.POST.get('color')
        if not color or not (color.startswith('#') and len(color) in (4,7)):
            return JsonResponse({'status':'error','message':'Color inválido.'}, status=400)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.neon_color = color
        profile.save()
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'unauthorized'}, status=401)


@login_required
def perfilView(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    pic_form   = ProfilePictureForm(instance=profile)

    # Logros
    all_achievements = Achievement.objects.all()
    unlocked_ids     = list(
        UserAchievement.objects
            .filter(user=request.user)
            .values_list('achievement_id', flat=True)
    )

    # Desafíos activos
    now    = timezone.now()
    active = Challenge.objects.filter(start__lte=now, end__gte=now)
    qs_prog = UserChallengeProgress.objects.filter(
        user=request.user,
        challenge__in=active
    ).select_related('challenge')

    challenges_progress = []
    for prog in qs_prog:
        target  = prog.challenge.target_value or 1
        percent = int((prog.progress / target) * 100)
        challenges_progress.append({
            'id':         prog.id,
            'name':       prog.challenge.name,
            'description':prog.challenge.description,
            'icon_url':   prog.challenge.icon.url,
            'progress':   prog.progress,
            'target':     prog.challenge.target_value,
            'completed':  prog.completed,
            'claimed':    prog.claimed,
            'percent':    percent,
        })

    # Skins
    all_skins   = Skin.objects.all()
    owned_skins = profile.owned_skins.all()
    owned_ids   = set(s.id for s in owned_skins)

    context = {
        'user':                 request.user,
        'profile_picture_form': pic_form,
        'neon_color':           profile.neon_color,
        'all_achievements':     all_achievements,
        'user_achievements':    unlocked_ids,
        'challenges_progress':  challenges_progress,
        'all_skins':            all_skins,
        'owned_skins':          owned_ids,
    }
    return render(request, 'perfil/profile.html', context)


@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Foto de perfil actualizada.")
        else:
            messages.error(request, "Error al subir la foto.")
    return redirect('Perfil')


@login_required
def claim_reward(request, progress_id):
    prog = get_object_or_404(
        UserChallengeProgress,
        id=progress_id,
        user=request.user,
        completed=True,
        claimed=False
    )
    with transaction.atomic():
        profile = request.user.userprofile
        profile.coins += 100
        profile.save()
        prog.claimed = True
        prog.save()
    messages.success(request, "¡Has recibido 100 monedas! 🎉")
    return redirect('Perfil')


@login_required
def equip_skin(request, skin_id):
    skin = get_object_or_404(Skin, id=skin_id)
    profile = request.user.userprofile
    if skin in profile.owned_skins.all():
        profile.active_skin = skin
        profile.save()
        messages.success(request, f"{skin.name} equipado.")
    return redirect('Perfil')
