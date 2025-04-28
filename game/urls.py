from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('play/<str:categoria_name>/<str:nivel_name>/', views.game_view, name='play'),
    path('seleccionar/', views.select_level_view, name='seleccionar'),
]