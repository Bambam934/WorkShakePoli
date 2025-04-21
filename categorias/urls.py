# categorias/urls.py
from django.urls import path
from . import views

app_name = 'categorias'

urlpatterns = [
    # Vista de selección en la raíz de este conjunto de URLs
    path('', views.select_level_view, name='select_level'),
    # Vista para procesar la selección y redirigir al juego
    path('start/', views.start_game_view, name='start_game'),
]