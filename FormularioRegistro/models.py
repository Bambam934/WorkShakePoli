from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, nombreUsuario, password=None):
        if not email:
            raise ValueError("El usuario debe tener un email")
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            nombreUsuario=nombreUsuario
        )
        user.set_password(password)  # Encripta la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, nombreUsuario, password):
        user = self.create_user(email, nombre, apellido, nombreUsuario, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Registro(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nombreUsuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  
    last_login = models.DateTimeField(default=timezone.now, null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="registro_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="registro_permissions", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'nombreUsuario']

    class Meta:
        default_manager_name = "objects"  # ✅ Agregado aquí

    def __str__(self):
        return str(self.email)

