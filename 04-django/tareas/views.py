from django.shortcuts import render, redirect, get_object_or_404
from .forms import TareaIndividualForm, TareaGrupalForm
from .models import Tarea
from usuarios.helpers import usuario_actual

def crear_tarea_individual(request):
    usuario = usuario_actual(request)
    if not usuario:
        return redirect("login")

    if request.method == "POST":
        form = TareaIndividualForm(request.POST, creador=usuario)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.tipo = "INDIVIDUAL"
            tarea.creador = usuario
            tarea.save()

            # Añadir automáticamente al creador como único colaborador
            tarea.colaboradores.add(usuario)

            return redirect("mis_tareas")
    else:
        form = TareaIndividualForm(creador=usuario)

    return render(request, "tareas/crear_tarea_individual.html", {"form": form})



def crear_tarea_grupal(request):
    usuario = usuario_actual(request)
    if not usuario:
        return redirect("login")
    
    if request.method == "POST":
        form = TareaGrupalForm(request.POST, creador=usuario)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.tipo = "GRUPAL"
            tarea.creador = usuario
            tarea.save()

            # Guardamos colaboradores seleccionados
            form.save_m2m()

            # Añadimos automáticamente al creador como colaborador
            tarea.colaboradores.add(usuario)

            return redirect("mis_tareas")
    else:
        form = TareaGrupalForm(creador=usuario)

    return render(request, "tareas/crear_tarea_grupal.html", {"form": form})


def mis_tareas(request):
    usuario = usuario_actual(request)
    if not usuario:
        return redirect("login")
    
    tareas_creadas = Tarea.objects.filter(creador=usuario)
    tareas_colabora = Tarea.objects.filter(colaboradores=usuario)

    return render(request, "tareas/mis_tareas.html", {
        "tareas_creadas": tareas_creadas,
        "tareas_colabora": tareas_colabora,
    })


def tareas_a_validar(request):
    usuario = usuario_actual(request)
    if not usuario:
        return redirect("login")
    
    tareas = Tarea.objects.filter(
        requiere_validacion_profesor=True,
        profesor_validador=usuario,
        completada_por_alumno=True,
        validada_por_profesor=False
    )

    return render(request, "tareas/tareas_a_validar.html", {"tareas": tareas})


def detalle_tarea(request, tarea_id):
    usuario = usuario_actual(request)
    if not usuario:
        return redirect("login")

    tarea = Tarea.objects.get(id=tarea_id)

    return render(request, "tareas/detalle_tarea.html", {
        "tarea": tarea,
        "usuario": usuario,
    })



def completar_tarea(request, tarea_id):
    usuario = usuario_actual(request)
    if not usuario:
        return redirect("login")

    tarea = Tarea.objects.get(id=tarea_id)

    tarea.completada_por_alumno = True
    tarea.save()

    return redirect("detalle_tarea", tarea_id=tarea.id)



def validar_tarea(request, tarea_id):
    usuario = usuario_actual(request)
    if not usuario:
        return redirect("login")

    tarea = Tarea.objects.get(id=tarea_id)

    tarea.validada_por_profesor = True
    tarea.save()

    return redirect("detalle_tarea", tarea_id=tarea.id)

