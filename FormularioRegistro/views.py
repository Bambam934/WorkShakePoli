from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import Registro
from django.contrib.auth.hashers import make_password 
def home(request):
    """
    Vista para la página de inicio.
    """
    return render(request, 'home.html')  # Renderiza la plantilla home.html



def registro(request):
    """
    Vista para manejar el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)  # Crea el formulario con los datos enviados
        if form.is_valid():
            # Guardar el registro en la base de datos
            nuevo_registro = form.save(commit=False)  # No guardar todavía para poder manipular los datos
            nuevo_registro.password = make_password(form.cleaned_data['password'])  # Encriptar la contraseña
            nuevo_registro.save()  # Ahora guarda en la base de datos
            return exito(request)  # Redirige a la vista 'exito'
        else:
            print("Formulario no válido:", form.errors)  # Depuración: muestra errores del formulario
    else:
        # Si no es una solicitud POST, mostrar el formulario vacío
        form = RegistroForm()
    
    # Renderizar la plantilla con el formulario
    return render(request, 'registro.html', {'form': form})
def exito(request):
    """
    Vista para mostrar una página de éxito después del registro.
    """
    return render(request, 'exito.html')