from django.urls import path
from .views import inicioSesion, inicioExitoso

urlpatterns = [
    path('iniciarSesion/', inicioSesion, name='inicioSesion'),
    path('sesionIniciada/', inicioExitoso, name='exito'),
]