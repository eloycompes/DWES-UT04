from django.shortcuts import render
from django.http import HttpResponse
import json

def usuario_view(request):

    # Datos del ejercicio 02 en formato JSON
    usuario_json = """
    {
        "nombre": "Laura",
        "apellidos": "Gómez Pérez",
        "dni": "12345678A",
        "email": "laura.gomez@example.com",
        "telefono": "654321987",
        "edad": 17,
        "pagos": {
            "enero": 20,
            "febrero": 20,
            "marzo": 20,
            "abril": 0,
            "mayo": 20,
            "junio": 20,
            "julio": 20,
            "agosto": 0,
            "septiembre": 20,
            "octubre": 20,
            "noviembre": 20,
            "diciembre": 20
        }
    }
    """

    # Convierto el JSON a diccionario de Python
    usuario = json.loads(usuario_json)

    total_pagado = sum(usuario["pagos"].values())

    # Determino el color según la edad
    color_edad = "green" if usuario["edad"] >= 18 else "red"

    # Tabla de pagos
    tabla = ""
    for mes, cantidad in usuario["pagos"].items():
        estado = "PAGADO" if cantidad > 0 else "PENDIENTE"
        color_fila = 'style="background-color:#f8d7da; color:#721c24;"' if cantidad == 0 else ""
        tabla += f"<tr {color_fila}><td>{mes.capitalize()}</td><td>{cantidad} €</td><td>{estado}</td></tr>"

    # HTML final (directamente en la vista)
    html = f"""
    <html>
        <head>
            <title>Datos del Usuario</title>
        </head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>Información personal</h1>
            <p><strong>Nombre:</strong> {usuario['nombre']}</p>
            <p><strong>Apellidos:</strong> {usuario['apellidos']}</p>
            <p><strong>DNI:</strong> {usuario['dni']}</p>
            <p><strong>Email:</strong> {usuario['email']}</p>
            <p><strong>Teléfono:</strong> {usuario['telefono']}</p>
            <p><strong>Edad:</strong> <span style='color:{color_edad}; font-weight:bold;'>{usuario['edad']}</span></p>

            <h2>Pagos mensuales</h2>
            <table border="1" cellpadding="6" cellspacing="0">
                <tr style="background-color:#007bff; color:white;">
                    <th>Mes</th>
                    <th>Importe (€)</th>
                    <th>Estado</th>
                </tr>
                {tabla}
                <tr>
                    <td><strong>Total pagado:</strong></td>
                    <td colspan="2"><strong>{total_pagado} €</strong></td>
                </tr>
            </table>
        </body>
    </html>
    """

    return HttpResponse(html)
