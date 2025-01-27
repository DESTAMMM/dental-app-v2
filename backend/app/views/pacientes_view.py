def render_paciente_list(pacientes):
    return [
        {
            "id_paciente": paciente.id_paciente,
            "usuario": {
                "id_usuario": paciente.usuario.id_usuario,
                "nombre_usuario": paciente.usuario.nombre_usuario,
                "nombre": paciente.usuario.nombre,
                "apellido": paciente.usuario.apellido,
                "correo_electronico": paciente.usuario.correo_electronico,
                "telefono": paciente.usuario.telefono,
                "rol": {
                    "id_rol": paciente.usuario.rol.id_rol,
                    "nombre_rol": paciente.usuario.rol.nombre_rol
                }
            },
            "fecha_nacimiento": paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
            "direccion": paciente.direccion
        }
        for paciente in pacientes
    ]


def render_paciente_detail(paciente):
    return {
        "id_paciente": paciente.id_paciente,
        "usuario": {
            "id_usuario": paciente.usuario.id_usuario,
            "nombre_usuario": paciente.usuario.nombre_usuario,
            "nombre": paciente.usuario.nombre,
            "apellido": paciente.usuario.apellido,
            "correo_electronico": paciente.usuario.correo_electronico,
            "telefono": paciente.usuario.telefono,
            "rol": {
                "id_rol": paciente.usuario.rol.id_rol,
                "nombre_rol": paciente.usuario.rol.nombre_rol
            }
        },
        "fecha_nacimiento": paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
        "direccion": paciente.direccion
    }
