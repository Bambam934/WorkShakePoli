from django.urls import path
from .views import home, registro, exito  # Importa la vista home
from FormularioInicioSesion import views

urlpatterns = [
    path('', home, name='home'),  # Ruta raíz
    path('registro/', registro, name='registro'),
    
    path('exito/', exito, name='exito'),
    path('iniciarSesion/', views.inicio,name='inicio'),
]