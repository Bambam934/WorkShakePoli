# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import RegistroForm
from datetime import date
from django.shortcuts import get_object_or_404
from .models import Registro

def registro(request):
    """
    Vista para manejar el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Crear una instancia del modelo sin guardarla en la base de datos
            nuevo_registro = form.save(commit=False)
            
            # Encriptar la contraseña antes de guardarla
            nuevo_registro.password = make_password(form.cleaned_data['password'])
            
            # Asignar la fecha actual al campo 'fecha'
            nuevo_registro.fecha = date.today()
            
            # Guardar el registro en la base de datos
            nuevo_registro.save()
            
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
    user = get_object_or_404(Registro, verification_token=token)
    
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

