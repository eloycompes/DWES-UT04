from django.shortcuts import render, redirect, get_object_or_404
from .forms import TareaIndividualForm, TareaGrupalForm
from .models import Tarea

def crear_tarea_individual(request):
    if request.method == "POST":
        form = TareaIndividualForm(request.POST, creador=request.user)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.tipo = "INDIVIDUAL"
            tarea.creador = request.user
            tarea.save()
            form.save_m2m()
            return redirect("mis_tareas")
    else:
        form = TareaIndividualForm(creador=request.user)

    return render(request, "tareas/crear_tarea_individual.html", {"form": form})


def crear_tarea_grupal(request):
    if request.method == "POST":
        form = TareaGrupalForm(request.POST, creador=request.user)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.tipo = "GRUPAL"
            tarea.creador = request.user
            tarea.save()

            # Guardamos colaboradores seleccionados
            form.save_m2m()

            # Añadimos automáticamente al creador como colaborador
            tarea.colaboradores.add(request.user)

            return redirect("mis_tareas")
    else:
        form = TareaGrupalForm(creador=request.user)

    return render(request, "tareas/crear_tarea_grupal.html", {"form": form})


def mis_tareas(request):
    tareas_creadas = Tarea.objects.filter(creador=request.user)
    tareas_colabora = Tarea.objects.filter(colaboradores=request.user)

    return render(request, "tareas/mis_tareas.html", {
        "tareas_creadas": tareas_creadas,
        "tareas_colabora": tareas_colabora,
    })


def tareas_a_validar(request):
    tareas = Tarea.objects.filter(
        requiere_validacion_profesor=True,
        profesor_validador=request.user,
        completada_por_alumno=True,
        validada_por_profesor=False
    )

    return render(request, "tareas/tareas_a_validar.html", {"tareas": tareas})


def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    return render(request, "tareas/detalle_tarea.html", {"tarea": tarea})


def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if not tarea.requiere_validacion_profesor:
        tarea.completada_por_alumno = True
        tarea.save()

    return redirect("mis_tareas")


def validar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if tarea.requiere_validacion_profesor and tarea.profesor_validador == request.user:
        tarea.validada_por_profesor = True
        tarea.save()

    return redirect("tareas_a_validar")
