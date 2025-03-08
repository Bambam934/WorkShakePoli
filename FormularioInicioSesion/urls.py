from django.urls import path
from .views import inicio, inicioExitoso
from FormularioRegistro import views

urlpatterns = [
    path('iniciarSesion/', inicio, name='inicioSesion'),
    path('inicioExitoso/', inicioExitoso, name='exito'),
    path('registro/', views.registro, name='registro'),
]