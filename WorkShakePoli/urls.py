from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FormularioRegistro.urls')),
    path('',include('FormularioInicioSesion.urls')),
    path('',include('game.urls')),
    

]
