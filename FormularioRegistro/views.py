from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.http import HttpResponse
from .models import Registro

def registro(request):
    """
    Vista para manejar el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
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

def verify_email(request, token):
    """
    Vista para verificar el correo electrónico del usuario.
    """
    # Buscar el usuario por el token de verificación
    try:
        user = Registro.objects.get(verification_token=token)
    except Registro.DoesNotExist:
        return HttpResponse("Token inválido o ya utilizado.", status=400)
    
    # Marcar el correo como verificado
    user.is_verified = True
    user.verification_token = None  # Eliminar el token después de la verificación
    user.save()
    
    # Mostrar una página de éxito
    return render(request, 'verificacion_exitosa.html')

def exito(request):
    """
    Vista para mostrar una página de éxito después del registro.
    """
    return render(request, 'exito.html')