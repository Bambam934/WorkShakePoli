# game/urls.py
from django.urls import path
from . import views
from . import api  
app_name = 'game'

urlpatterns = [
    path('play/<str:categoria_name>/<str:nivel_name>/', views.game_view, name='play'),
    path('api/partida/', api.registrar_partida, name='registrar_partida'),
]
