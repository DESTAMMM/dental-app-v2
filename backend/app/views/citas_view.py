def render_citas_list(citas):
    return [
        {
            "id_cita": cita.id_cita,
            "fecha_cita": cita.fecha_cita.strftime('%Y-%m-%d'),
            "hora_cita": cita.hora_cita.strftime('%H:%M:%S'),
            "motivo_cita": cita.motivo_cita,
            "estado": cita.estado,
            "paciente": {
                "id_paciente": cita.paciente.id_paciente,
                "nombre": cita.paciente.usuario.nombre,
                "apellido": cita.paciente.usuario.apellido
            },
            "doctor": {
                "id_doctor": cita.doctor.id_doctor if cita.doctor else None,
                "nombre": cita.doctor.usuario.nombre if cita.doctor else None,
                "apellido": cita.doctor.usuario.apellido if cita.doctor else None
            }
        }
        for cita in citas
    ]

def render_cita_detail(cita):
    return {
        "id_cita": cita.id_cita,
        "fecha_cita": cita.fecha_cita.strftime('%Y-%m-%d'),
        "hora_cita": cita.hora_cita.strftime('%H:%M:%S'),
        "motivo_cita": cita.motivo_cita,
        "estado": cita.estado,
        "paciente": {
            "id_paciente": cita.paciente.id_paciente,
            "nombre": cita.paciente.usuario.nombre,
            "apellido": cita.paciente.usuario.apellido
        },
        "doctor": {
            "id_doctor": cita.doctor.id_doctor if cita.doctor else None,
            "nombre": cita.doctor.usuario.nombre if cita.doctor else None,
            "apellido": cita.doctor.usuario.apellido if cita.doctor else None
        }
    }
