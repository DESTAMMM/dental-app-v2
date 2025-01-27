def render_asistente_list(asistentes):
    return [
        {
            "id_asistente": asistente.id_asistente,
            "usuario": {
                "id_usuario": asistente.usuario.id_usuario,
                "nombre_usuario": asistente.usuario.nombre_usuario,
                "nombre": asistente.usuario.nombre,
                "apellido": asistente.usuario.apellido,
                "correo_electronico": asistente.usuario.correo_electronico,
                "telefono": asistente.usuario.telefono,
                "rol": {
                    "id_rol": asistente.usuario.rol.id_rol,
                    "nombre_rol": asistente.usuario.rol.nombre_rol
                }
            },
            "fecha_contratacion": asistente.fecha_contratacion.strftime('%Y-%m-%d'),
            "turno": asistente.turno,
            "area_especialidad": asistente.area_especialidad
        }
        for asistente in asistentes
    ]


def render_asistente_detail(asistente):
    return {
        "id_asistente": asistente.id_asistente,
        "usuario": {
            "id_usuario": asistente.usuario.id_usuario,
            "nombre_usuario": asistente.usuario.nombre_usuario,
            "nombre": asistente.usuario.nombre,
            "apellido": asistente.usuario.apellido,
            "correo_electronico": asistente.usuario.correo_electronico,
            "telefono": asistente.usuario.telefono,
            "rol": {
                "id_rol": asistente.usuario.rol.id_rol,
                "nombre_rol": asistente.usuario.rol.nombre_rol
            }
        },
        "fecha_contratacion": asistente.fecha_contratacion.strftime('%Y-%m-%d'),
        "turno": asistente.turno,
        "area_especialidad": asistente.area_especialidad
    }
