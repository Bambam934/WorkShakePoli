from django.urls import path
from perfil import views
from .views import update_neon_color

urlpatterns = [
    path('perfil/', views.perfilView, name='Perfil'),
    path('upload_profile_picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('update-color/', update_neon_color, name='update_neon_color'),
]
