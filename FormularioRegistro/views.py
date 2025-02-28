from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import RegistroForm


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nuevo_registro = form.save(commit=False)
            nuevo_registro.password = make_password(form.cleaned_data['password'])  # Encripta la contraseña
            nuevo_registro.save()
            return redirect('exito')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def exito(request):
    return render(request, 'exito.html')
