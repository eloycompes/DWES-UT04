from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'dni', 'rol']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este email.")
        return email

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Ya existe un usuario con este DNI.")
        return dni
