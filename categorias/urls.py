from django.urls import path
from .views import select_level_view, start_game_view

app_name = 'categorias'

urlpatterns = [
    path('seleccionar/', select_level_view, name='select_level'),
    path('start/', start_game_view, name='start_game'),
]