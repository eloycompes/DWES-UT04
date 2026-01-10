from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm

def lista_usuarios(request):
    alumnos = Usuario.objects.filter(rol="ALUMNO")
    profesores = Usuario.objects.filter(rol="PROFESOR")
    return render(request, "usuarios/lista_usuarios.html", {
        "alumnos": alumnos,
        "profesores": profesores
    })


def alta_usuario(request):
    if request.method == "POST": # Nos envian datos desde el formulario para crear un usuario
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios") # vista que muestra todos
    else:
        form = UsuarioForm()

    return render(request, "usuarios/alta_usuario.html", {"form": form})

def datos_usuario(request, usuario_id):
    # Obtiene el usuario según su id; si no existe, devuelve un 404
    usuario = get_object_or_404(Usuario, id=usuario_id)

    return render(request, "usuarios/datos_usuario.html", {"usuario": usuario})



def login_view(request):
    if request.method == "POST":
        usuario_id = request.POST.get("usuario_id")
        request.session["usuario_id"] = usuario_id
        return redirect("mis_tareas")  # o donde quieras

    usuarios = Usuario.objects.all()
    return render(request, "usuarios/login.html", {"usuarios": usuarios})


def logout_view(request):
    request.session.flush()
    return redirect("login")
