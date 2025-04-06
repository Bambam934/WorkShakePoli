from django.urls import path
from . import views
from .views import game_view
from django.urls import path
from . import views

urlpatterns = [
    path('seleccionar/', views.select_level_view, name='seleccionar'),
    path('game/', game_view, name='game'),
    path('', views.index, name='index'),
    path('game/<str:categoria>/', views.levels_view, name='levels'),
    path('game/<str:categoria>/<str:nivel>/', views.game_view, name='game'),
]
