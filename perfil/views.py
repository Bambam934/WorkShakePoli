from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilePictureForm

@login_required
def perfilView(request):
    profile = request.user.userprofile
    profile_picture_form = ProfilePictureForm(instance=profile)
    context = {'profile_picture_form': profile_picture_form}
    return render(request, 'perfil.html', context)

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        print(f"Formulario enviado: {form.data}")  # Imprime los datos del formulario
        print(f"Archivos enviados: {request.FILES}") # Imprime los archivos enviados
        if form.is_valid():
            print("Formulario válido")
            form.save()
            print("Formulario guardado")
            return redirect('Perfil')
        else:
            print(f"Formulario inválido. Errores: {form.errors}") # Imprime los errores del formulario
    return redirect('Perfil')