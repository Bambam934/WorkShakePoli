from django.db import models
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class Registro(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)
    is_verified = models.BooleanField(default=False)  # Para verificar el correo
    verification_token = models.CharField(max_length=100, blank=True, null=True)  # Token de verificación
    objects = models.Manager()  # Añadir el manager por defecto

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        # Encriptar la contraseña antes de guardar
        if not self.pk:  # Solo si es un nuevo registro
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def send_verification_email(self):
        # Generar un token único para la verificación
        token = get_random_string(50)
        self.verification_token = token
        self.save()

        # Crear el enlace de verificación
        verification_link = f"http://tudominio.com/verify-email/{token}/"

        # Personalizar el nombre del remitente
        from_email = '"Wordshake Team" <tucorreo@gmail.com>'  # Nombre del remitente y dirección de correo

        # Enviar el correo electrónico
        send_mail(
            'Verifica tu correo electrónico',
            f'Haz clic en el siguiente enlace para verificar tu correo: {verification_link}',
            'tucorreo@gmail.com',  # Remitente
            [self.email],  # Destinatario
            fail_silently=False,
        )