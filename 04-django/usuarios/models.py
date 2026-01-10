from django.db import models
from django.core.exceptions import ValidationError
import uuid
import re

# Create your models here.
class Usuario(models.Model):
    ROLES = [('ALUMNO', 'Alumno'), ('PROFESOR', 'Profesor')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=9, unique=True)
    rol = models.CharField(max_length=10, choices=ROLES)

    def clean(self):
        # Validación DNI (8 números + 1 letra)
        if not re.match(r'^\d{8}[A-Za-z]$', self.dni):
            raise ValidationError("El DNI debe tener 8 números y una letra final.")

        # Validación rol (aunque choices ya lo controla)
        if self.rol not in dict(self.ROLES):
            raise ValidationError("El rol debe ser ALUMNO o PROFESOR.")


    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"