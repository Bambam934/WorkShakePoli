from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilePictureForm # Asegúrate que este formulario esté definido
from .models import UserProfile # Importa el modelo UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Considera las implicaciones de seguridad

@csrf_exempt # Revisa si puedes quitar esto si el token CSRF se maneja correctamente
def update_neon_color(request):
    if request.method == 'POST' and request.user.is_authenticated:
        color = request.POST.get('color')
        if not color: # Validación básica del color
            return JsonResponse({'status': 'error', 'message': 'Color no proporcionado.'}, status=400)
        # Validar formato de color (ej: #RRGGBB o #RGB)
        if not (color.startswith('#') and (len(color) == 7 or len(color) == 4)):
             return JsonResponse({'status': 'error', 'message': 'Formato de color inválido.'}, status=400)


        # Usar get_or_create para asegurar que el perfil exista
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.neon_color = color
        profile.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'unauthorized'}, status=401)

@login_required
def perfilView(request):
    # Usar get_or_create para asegurar que el perfil exista
    # Si el perfil no existe, se creará con el color neón por defecto del modelo.
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    profile_picture_form = ProfilePictureForm(instance=profile)
    context = {
        'user': request.user, # Añadir user al contexto explícitamente es buena práctica
        'profile_picture_form': profile_picture_form,
        'neon_color': profile.neon_color # Este es el color que se usará en la plantilla
    }
    return render(request, 'perfil.html', context)

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        print(f"Formulario enviado: {form.data}")
        print(f"Archivos enviados: {request.FILES}")
        if form.is_valid():
            print("Formulario válido")
            form.save()
            print("Formulario guardado")
            return redirect('Perfil') # Asegúrate que 'Perfil' sea el nombre correcto de tu URL
        else:
            print(f"Formulario inválido. Errores: {form.errors}")
    return redirect('Perfil') # O manejar el error de alguna otra forma