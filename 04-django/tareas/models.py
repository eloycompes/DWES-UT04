from django.db import models
from usuarios.models import Usuario

class Tarea(models.Model):
    TIPOS = [
        ('INDIVIDUAL', 'Individual'),
        ('GRUPAL', 'Grupal'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_entrega = models.DateField(null=True, blank=True)

    tipo = models.CharField(max_length=10, choices=TIPOS)

    # Propiedad: si requiere validación del profesor
    requiere_validacion_profesor = models.BooleanField(default=False)

    # Creador (puede ser alumno o profesor)
    creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="tareas_creadas"
    )

    # Colaboradores (solo alumnos)
    colaboradores = models.ManyToManyField(
        Usuario,
        related_name="tareas_colabora",
        blank=True,
        limit_choices_to={'rol': 'ALUMNO'}
    )

    # Profesor que valida (solo si requiere validación)
    profesor_validador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas_a_validar",
        limit_choices_to={'rol': 'PROFESOR'}
    )

    # Estado
    completada_por_alumno = models.BooleanField(default=False)
    validada_por_profesor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"
