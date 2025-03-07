from django.urls import path
from .views import inicio, inicioExitoso

urlpatterns = [
    path('iniciarSesion/', inicio, name='inicioSesion'),
    path('inicioExitoso/', inicioExitoso, name='exito'),
]