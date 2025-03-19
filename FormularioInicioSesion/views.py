from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ResetPasswordRequestSerializer, ResetPasswordSerializer
from .forms import InicioSesionForm
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

def inicio(request):
    remembered_email = request.COOKIES.get('remembered_email', '')

    if request.method == "POST":
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                response = redirect('inicioExitoso')

                if form.cleaned_data.get('remember_me'):
                    response.set_cookie('remembered_email', email, max_age=30*24*60*60)
                else:
                    response.delete_cookie('remembered_email')

                return response
            else:
                form.add_error(None, "Correo o contraseña incorrectos")  # Mensaje correcto para login
    else:
        form = InicioSesionForm(initial={'email': remembered_email})

    return render(request, 'inicio.html', {'form': form})


def inicioExitoso(request):
    """ Muestra la pantalla de inicio de sesión exitoso y permite ir al juego """
    return render(request, 'inicioExitoso.html')


@login_required
def game_view(request):
    """ Carga el juego en una nueva página independiente """
    return render(request, 'game.html')


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def get(self, request):
        return render(request, "password_reset.html")  # Mostrar el formulario

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"http://localhost:8000/reset/{uid}/{token}/"

                send_mail(
                    'Restablecimiento de contraseña',
                    f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}',
                    'from@example.com',  # Cambia esto por tu dirección de correo
                    [email],
                    fail_silently=False,
                )
                return Response({'success': 'Se ha enviado un enlace para restablecer la contraseña'}, status=200)
            except User.DoesNotExist:
                return Response({'error': 'No se encontró un usuario con ese correo electrónico.'}, status=404)
        return Response(serializer.errors, status=400)

class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = PasswordResetTokenGenerator()
        if user is not None and token_generator.check_token(user, token):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data['new_password']
                user.set_password(new_password)
                user.save()
                return Response({'success': 'Contraseña actualizada'}, status=200)
            return Response(serializer.errors, status=400)
        return Response({'error': 'El enlace de restablecimiento de contraseña es inválido o ha expirado.'}, status=400)

class CustomPasswordResetView(PasswordResetView):
    template_name = "password_reset_form.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "El correo ingresado no está registrado.")
            return redirect("password_reset")
        return super().form_valid(form)

def registro(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("registro")

        if len(password) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
            return redirect("registro")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect("registro")

        user = User.objects.create_user(username=email, email=email, password=password)
        messages.success(request, "Registro exitoso.")
        return redirect("inicio")
