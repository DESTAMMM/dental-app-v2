def render_paciente_list(pacientes):
    # Devuelve una lista de pacientes con información adicional.
    return [
        {
            "id_paciente": paciente.id_paciente,
            "id_usuario": paciente.id_usuario,
            "nombre_usuario": paciente.usuario.nombre_usuario,
            "nombre": paciente.usuario.nombre,
            "apellido": paciente.usuario.apellido,
            "correo_electronico": paciente.usuario.correo_electronico,
            "fecha_nacimiento": paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
            "direccion": paciente.direccion,
        }
        for paciente in pacientes
    ]
def render_paciente_detail(paciente):
    #Devuelve el detalle de un paciente individual.
    return {
        "id_paciente": paciente.id_paciente,
        "id_usuario": paciente.id_usuario,
        "nombre_usuario": paciente.usuario.nombre_usuario,
        "nombre": paciente.usuario.nombre,
        "apellido": paciente.usuario.apellido,
        "correo_electronico": paciente.usuario.correo_electronico,
        "fecha_nacimiento": paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
        "direccion": paciente.direccion,
    }
