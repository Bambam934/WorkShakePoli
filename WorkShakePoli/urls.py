from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FormularioRegistro.urls')),
    path('',include('FormularioInicioSesion.urls')),
    path('game/', include('game.urls', namespace='game')),
    path('select/', include('categorias.urls', namespace='categorias')),

]
