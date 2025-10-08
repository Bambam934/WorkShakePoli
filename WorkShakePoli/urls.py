# WordShakePoli/urls.py  (urls.py “raíz” del proyecto)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


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
    
    path('logros/', include('achievements.urls', namespace='achievements')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include(("game.urls", "game_api"), namespace="game_api")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]
    


# Archivos multimedia en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
