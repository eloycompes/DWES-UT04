from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'dni', 'rol')
    search_fields = ('nombre', 'apellido', 'email', 'dni')
    list_filter = ('rol',)

