from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_usuarios, name="lista_usuarios"),
    path("alta/", views.alta_usuario, name="alta_usuario"),

]
