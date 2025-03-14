from django.urls import path
from django.contrib.auth import views as auth_views
from .views import inicio, inicioExitoso, CustomPasswordResetView
from FormularioRegistro import views
from game.views import game_view 

urlpatterns = [
    path('iniciarSesion/', inicio, name='inicioSesion'),
    path('inicioExitoso/', inicioExitoso, name='inicioExitoso'),
    path('registro/', views.registro, name='registro'),
    path('', views.home, name='home'),
     path('game/', game_view, name='game'),

   
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
