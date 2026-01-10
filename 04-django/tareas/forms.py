from django import forms
from .models import Tarea
from usuarios.models import Usuario

class TareaBaseForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = [
            "titulo",
            "descripcion",
            "fecha_entrega",
            "requiere_validacion_profesor",
            "profesor_validador",
            "colaboradores",
        ]

    def __init__(self, *args, **kwargs):
        self.creador = kwargs.pop("creador")  # lo pasaremos desde la vista
        super().__init__(*args, **kwargs)

        # Filtrar profesores para el validador
        self.fields["profesor_validador"].queryset = Usuario.objects.filter(rol="PROFESOR")

        # Filtrar alumnos para colaboradores
        self.fields["colaboradores"].queryset = Usuario.objects.filter(rol="ALUMNO")

        # Si no requiere validación → ocultar profesor_validador
        if not self.initial.get("requiere_validacion_profesor", False):
            self.fields["profesor_validador"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()

        requiere = cleaned_data.get("requiere_validacion_profesor")
        profesor = cleaned_data.get("profesor_validador")

        # Si requiere validación → debe haber profesor validador
        if requiere and not profesor:
            raise forms.ValidationError("Debes seleccionar un profesor validador.")

        return cleaned_data


class TareaIndividualForm(TareaBaseForm):
    class Meta(TareaBaseForm.Meta):
        pass

    def clean(self):
        cleaned_data = super().clean()

        colaboradores = cleaned_data.get("colaboradores")

        # Solo 1 colaborador permitido
        if colaboradores.count() > 1:
            raise forms.ValidationError("Una tarea individual solo puede tener un alumno asignado.")

        return cleaned_data


class TareaGrupalForm(TareaBaseForm):
    class Meta(TareaBaseForm.Meta):
        pass

    def clean(self):
        cleaned_data = super().clean()

        colaboradores = cleaned_data.get("colaboradores")

        # Mínimo 2 alumnos (creador se añadirá luego)
        if colaboradores.count() < 1:
            raise forms.ValidationError("Una tarea grupal debe tener al menos dos alumnos (incluyendo al creador).")

        return cleaned_data
