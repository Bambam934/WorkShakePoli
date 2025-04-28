from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FormularioRegistro.urls')),
    path('',include('FormularioInicioSesion.urls')),

    path('game/', include(('game.urls','game'), namespace='game')),

    path('select/', include('categorias.urls', namespace='categorias')),
    path('game/', include('game.urls')),
    path('',include('game.urls')),
    path('',include('perfil.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
