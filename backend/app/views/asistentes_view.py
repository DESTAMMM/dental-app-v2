def render_asistente_list(asistentes):

    # Devuelve una lista de asistentes con información adicional.
    return [
        {
            "id_asistente": asistente.id_asistente,
            "id_usuario": asistente.id_usuario,
            "nombre_usuario": asistente.usuario.nombre_usuario,
            "nombre": asistente.usuario.nombre,
            "apellido": asistente.usuario.apellido,
            "correo_electronico": asistente.usuario.correo_electronico,
            "fecha_contratacion": asistente.fecha_contratacion.strftime('%Y-%m-%d'),
            "turno": asistente.turno,
            "area_especialidad": asistente.area_especialidad,
        }
        for asistente in asistentes
    ]


def render_asistente_detail(asistente):
    # Devuelve el detalle de un asistente individual.
    return {
        "id_asistente": asistente.id_asistente,
        "id_usuario": asistente.id_usuario,
        "nombre_usuario": asistente.usuario.nombre_usuario,
        "nombre": asistente.usuario.nombre,
        "apellido": asistente.usuario.apellido,
        "correo_electronico": asistente.usuario.correo_electronico,
        "fecha_contratacion": asistente.fecha_contratacion.strftime('%Y-%m-%d'),
        "turno": asistente.turno,
        "area_especialidad": asistente.area_especialidad,
    }
