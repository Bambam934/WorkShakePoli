# game/urls.py
from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    # Única ruta para la pantalla de juego real
    path('play/<str:categoria_name>/<str:nivel_name>/', views.game_view, name='play'),
    # Considera añadir URLs para AJAX si las implementas
    # path('ajax/validate_word/', views.validate_word_ajax, name='validate_word_ajax'),
]