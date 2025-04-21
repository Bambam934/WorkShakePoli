# game/urls.py
from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [

    # Única ruta para la pantalla de juego real
    path('play/<str:categoria_name>/<str:nivel_name>/', views.game_view, name='play'),
    # Considera añadir URLs para AJAX si las implementas
    # path('ajax/validate_word/', views.validate_word_ajax, name='validate_word_ajax'),]
    path('seleccionar/', views.select_level_view, name='seleccionar'),
    path('game/', game_view, name='game'),
    path('', views.index, name='index'),
    path('game/<str:categoria>/', views.levels_view, name='levels'),
    path('game/<str:categoria_id>/<str:nivel>/', views.game_view, name='game'),


]