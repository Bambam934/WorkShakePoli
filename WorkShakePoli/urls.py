# WordShakePoli/urls.py  (urls.py “raíz” del proyecto)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Registro / Login
    path('',  include('FormularioRegistro.urls')),
    path('',  include('FormularioInicioSesion.urls')),

    # Perfil de usuario (con prefijo y namespace)
    path("perfil/", include(("perfil.urls", "perfil"), namespace="perfil")),

    # Categorías / Juego
    path('categorias/', include(('categorias.urls', 'categorias'),
                                namespace='categorias')),
    path('game/', include(('game.urls', 'game'), namespace='game')),

    # Logros
    path("achievements/", include("achievements.urls")),
    path('logros/', include('achievements.urls', namespace='achievements')),
    
]

# Archivos multimedia en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
