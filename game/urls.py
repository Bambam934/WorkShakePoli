# game/urls.py
from django.urls import path
from . import views
from . import api  # si ya usas api.registrar_partida
from .views import CancelGameView, CreateGameView, SubmitWordView, FinishGameView, GetGameView, ListMyGamesView

app_name = 'game'

urlpatterns = [
    # HTML del juego
    path('play/<str:categoria_name>/<str:nivel_name>/', views.game_view, name='play'),
    path('api/partida/', api.registrar_partida, name='registrar_partida'),
    

    # REST API v1 (SOA fachada)
    path("api/v1/games", CreateGameView.as_view(), name="create-game"),
    path("api/v1/games/<int:game_id>/submit", SubmitWordView.as_view(), name="submit"),
    path("api/v1/games/<int:game_id>/finish", FinishGameView.as_view(), name="finish"),
    path("api/v1/games/<int:game_id>", GetGameView.as_view(), name="get-game"),
    path("api/v1/games/mine", ListMyGamesView.as_view(), name="list-my-games"),
    path("api/v1/games/<int:game_id>/cancel", CancelGameView.as_view(), name="cancel"),

]
