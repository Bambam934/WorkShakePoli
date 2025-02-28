from django.db import models


# Create your models here.from django.db import models

class Registro(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)
    
    objects = models.Manager()