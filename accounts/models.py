from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, correo_electronico, nombre_de_usuario, edad=0, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError("El correo electrónico es obligatorio.")
        if not nombre_de_usuario:
            raise ValueError("El nombre de usuario es obligatorio.")
        
        correo_electronico = self.normalize_email(correo_electronico)
        user = self.model(
            correo_electronico=correo_electronico,
            nombre_de_usuario=nombre_de_usuario,
            edad=edad,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, nombre_de_usuario, edad=0, password=None, **extra_fields):
        extra_fields.setdefault('es_superusuario', True)
        extra_fields.setdefault('es_personal', True)
        extra_fields.setdefault('esta_activo', True)

        if extra_fields.get('es_superusuario') is not True:
            raise ValueError("El superusuario debe tener es_superusuario=True.")
        if extra_fields.get('es_personal') is not True:
            raise ValueError("El superusuario debe tener es_personal=True.")

        return self.create_user(correo_electronico, nombre_de_usuario, edad, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    nombre_de_usuario = models.CharField(max_length=150, unique=True)
    correo_electronico = models.EmailField(unique=True)
    edad = models.PositiveIntegerField(default=0)
    es_superusuario = models.BooleanField(default=False)
    es_personal = models.BooleanField(default=False)
    esta_activo = models.BooleanField(default=True)
    fecha_union = models.DateTimeField(default=now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre_de_usuario', 'edad']

    def __str__(self):
        return self.nombre_de_usuario

    def has_perm(self, perm, obj=None):
        """Indica si el usuario tiene un permiso específico."""
        return self.es_superusuario

    def has_module_perms(self, app_label):
        """Indica si el usuario tiene permisos para ver la app especificada."""
        return self.es_superusuario

    @property
    def is_staff(self):
        """Indica si el usuario es parte del personal administrativo."""
        return self.es_personal

    @property
    def is_active(self):
        """Indica si el usuario está activo."""
        return self.esta_activo

    

# Create your models here.
