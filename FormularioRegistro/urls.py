from django.urls import path
from .views import registro, verify_email, exito

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('exito/', exito, name='exito'),
]