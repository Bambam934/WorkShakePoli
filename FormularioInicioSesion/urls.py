from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import inicio, inicioExitoso, registro, CustomPasswordResetView
from game.views import game_view  
from FormularioRegistro.views import home  
from perfil.views import perfilView

urlpatterns = [
    # Rutas principales
    path('iniciarSesion/', inicio, name='inicioSesion'),
    path('inicioExitoso/', inicioExitoso, name='inicioExitoso'),
    path('registro/', registro, name='registro'),
    path('', home, name='home'),  # Página principal corregida
    path('game/', game_view, name='game'),  
    # Rutas para recuperación de contraseña
    path('reset_password/', CustomPasswordResetView.as_view(
        template_name="password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
    ), name='password_reset'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"), name='password_reset_complete'),
]
