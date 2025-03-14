from django.urls import path
from . import views
from .views import game_view

urlpatterns = [
    path('game/', game_view, name='game'),
    path('', views.index, name='index'),
]
