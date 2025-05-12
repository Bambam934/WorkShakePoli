# achievements/urls.py
from django.urls import path
from . import views

app_name = 'achievements'

urlpatterns = [
    path('claim/<int:progress_id>/', views.claim_reward, name='claim'),
]
