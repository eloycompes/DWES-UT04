from django.urls import path
from . import views

urlpatterns = [
    path("crear/individual/", views.crear_tarea_individual, name="crear_tarea_individual"),
    path("crear/grupal/", views.crear_tarea_grupal, name="crear_tarea_grupal"),

    path("mis-tareas/", views.mis_tareas, name="mis_tareas"),
    path("a-validar/", views.tareas_a_validar, name="tareas_a_validar"),

    path("<int:tarea_id>/", views.detalle_tarea, name="detalle_tarea"),
    path("<int:tarea_id>/completar/", views.completar_tarea, name="completar_tarea"),
    path("<int:tarea_id>/validar/", views.validar_tarea, name="validar_tarea"),
]
