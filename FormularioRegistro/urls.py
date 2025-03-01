from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('exito/', views.exito, name='exito'),
]