def render_doctor_list(doctores):
    # Devuelve una lista de doctores con información adicional.
    return [
        {
            "id_doctor": doctor.id_doctor,
            "id_usuario": doctor.id_usuario,
            "nombre_usuario": doctor.usuario.nombre_usuario,
            "nombre": doctor.usuario.nombre,
            "apellido": doctor.usuario.apellido,
            "correo_electronico": doctor.usuario.correo_electronico,
            "especialidad": doctor.especialidad,
        }
        for doctor in doctores
    ]
def render_doctor_detail(doctor):
    # Devuelve el detalle de un doctor individual.
    return {
        "id_doctor": doctor.id_doctor,
        "id_usuario": doctor.id_usuario,
        "nombre_usuario": doctor.usuario.nombre_usuario,
        "nombre": doctor.usuario.nombre,
        "apellido": doctor.usuario.apellido,
        "correo_electronico": doctor.usuario.correo_electronico,
        "especialidad": doctor.especialidad,
    }
