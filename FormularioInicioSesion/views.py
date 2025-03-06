from django.shortcuts import render
from .models import Inicio
from django.http import HttpResponse

# Create your views here.
def inicioSesion(request):
    """
    Vista para manejar el inicio de sesion
    """
    if request.method == 'POST':
        form = Inicio(request.POST)
        if form.is_valid():
            # Guardar el registro en la base de datos
            nuevo_registro = form.save()
            
            # Enviar el correo de verificación
            nuevo_registro.send_verification_email()
            
            # Redirigir a la página de éxito
            return redirect('exito')  # Asegúrate de que 'exito' esté en urls.py
    else:
        # Si no es una solicitud POST, mostrar el formulario vacío
        form = RegistroForm()
    
    # Renderizar la plantilla con el formulario
    return render(request, 'registro.html', {'form': form})
def inicioExitoso(request):
    """
    Vista para mostrar una página de éxito después del registro.
    """
    return render(request, 'inicioExito.html')