def render_doctor_list(doctores):
    return [
        {
            "id_doctor": doctor.id_doctor,
            "usuario": {
                "id_usuario": doctor.usuario.id_usuario,
                "nombre_usuario": doctor.usuario.nombre_usuario,
                "nombre": doctor.usuario.nombre,
                "apellido": doctor.usuario.apellido,
                "correo_electronico": doctor.usuario.correo_electronico,
                "telefono": doctor.usuario.telefono,
                "rol": {
                    "id_rol": doctor.usuario.rol.id_rol,
                    "nombre_rol": doctor.usuario.rol.nombre_rol
                }
            },
            "especialidad": doctor.especialidad,
            "numero_colegiatura": doctor.numero_colegiatura
        }
        for doctor in doctores
    ]


def render_doctor_detail(doctor):
    return {
        "id_doctor": doctor.id_doctor,
        "usuario": {
            "id_usuario": doctor.usuario.id_usuario,
            "nombre_usuario": doctor.usuario.nombre_usuario,
            "nombre": doctor.usuario.nombre,
            "apellido": doctor.usuario.apellido,
            "correo_electronico": doctor.usuario.correo_electronico,
            "telefono": doctor.usuario.telefono,
            "rol": {
                "id_rol": doctor.usuario.rol.id_rol,
                "nombre_rol": doctor.usuario.rol.nombre_rol
            }
        },
        "especialidad": doctor.especialidad,
        "numero_colegiatura": doctor.numero_colegiatura
    }
