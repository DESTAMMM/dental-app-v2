def render_user_list(usuarios):
    return [
        {
            "id_usuario": usuario.id_usuario,
            "nombre_usuario": usuario.nombre_usuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "correo_electronico": usuario.correo_electronico,
            "telefono": usuario.telefono,
            "rol": usuario.rol.nombre_rol
        } for usuario in usuarios
    ]

def render_user_detail(usuario):
    return {
        "id_usuario": usuario.id_usuario,
        "nombre_usuario": usuario.nombre_usuario,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "correo_electronico": usuario.correo_electronico,
        "telefono": usuario.telefono,
        "rol": usuario.rol.nombre_rol
    }
