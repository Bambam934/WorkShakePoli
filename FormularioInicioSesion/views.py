
from django.shortcuts import render
from .forms import InicioSesionForm  # Asegúrate de importar correctamente el formulario

def inicio(request):
    if request.method == "POST":
        form = InicioSesionForm(request.POST)  # Usa la nueva clase del formulario
        if form.is_valid():
            # Aquí podrías autenticar al usuario (lógica de autenticación)
            return render(request, 'inicioExitoso.html')  # Redirigir a la página de éxito
    else:
        form = InicioSesionForm()  # Instancia vacía del formulario

    return render(request, 'inicio.html', {'form': form})


def inicioExitoso(request):
    """
    Vista para mostrar una página de éxito después del registro.
    """
    return render(request, 'inicioExitoso.html')