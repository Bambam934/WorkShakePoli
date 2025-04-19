from django.urls import path
from perfil import views


urlpatterns = [
    path('perfil/', views.perfilView, name='Perfil'),
    path('upload_profile_picture/', views.upload_profile_picture, name='upload_profile_picture'),
]
