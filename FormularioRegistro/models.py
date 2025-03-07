from django.db import models

class Registro(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10)
    password = models.CharField(max_length=128)  # Asegúrate de que este campo sea lo suficientemente largo para almacenar contraseñas encriptadas

    def __str__(self):
        return f"{self.nombre} {self.apellido}"  # Devuelve una cadena que representa el objeto