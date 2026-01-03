from django.shortcuts import render
from .models import Usuario

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuarios/lista_usuarios.html", {"usuarios": usuarios})

def crear_usuario(request):
    if request.method == "POST": # Nos envian datos desde el formulario para crear un usuario
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios") # o la vista que muestra todos
    else:
        form = UsuarioForm()
    return render(request, "usuarios/crear_usuario.html", {"form": form})