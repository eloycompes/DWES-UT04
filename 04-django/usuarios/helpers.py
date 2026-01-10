from usuarios.models import Usuario

def usuario_actual(request):
    usuario_id = request.session.get("usuario_id")
    if usuario_id:
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return None
    return None
