# achievements/urls.py
from django.urls import path
from . import views
from .views import LeaderboardView
from django.urls import path
from .views import LeaderboardView, claim_reward, debug_send
app_name = 'achievements'

urlpatterns = [
    path("api/v1/leaderboards", LeaderboardView.as_view(), name="leaderboards"),
    path("claim/<int:progress_id>/", claim_reward, name="claim"),
    path("debug-send/", debug_send, name="debug_send"),
]
