# WordShakePoli/urls.py  (urls.py “raíz” del proyecto)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Registro / Inicio de sesión
    path('',  include('FormularioRegistro.urls')),
    path('',  include('FormularioInicioSesion.urls')),

    # Perfil de usuario
    path('',  include('perfil.urls')),

    # Categorías y niveles (selección)
    path('categorias/', include(('categorias.urls', 'categorias'),
                                namespace='categorias')),

    # Juego (partida)
    path('game/', include(('game.urls', 'game'), namespace='game')),
]

# Archivos multimedia (solo en desarrollo)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
