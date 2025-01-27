def render_citas_list(citas):
    return [
        {
            "id": cita.id,
            "fecha": cita.fecha,
            "hora": cita.hora,
            "doctor_id": cita.doctor_id,
            "paciente_id": cita.paciente_id,
            "motivo": cita.motivo,
            "estado": cita.estado,
        }
        for cita in citas
    ]

def render_cita_detail(cita):
    return {
        "id": cita.id,
        "fecha": cita.fecha,
        "hora": cita.hora,
        "doctor_id": cita.doctor_id,
        "paciente_id": cita.paciente_id,
        "motivo": cita.motivo,
        "estado": cita.estado,
    }