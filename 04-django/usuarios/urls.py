from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_usuarios, name="lista_usuarios"),
    path("alta/", views.alta_usuario, name="alta_usuario"),
    path("<uuid:usuario_id>/", views.datos_usuario, name="datos_usuario"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

]
