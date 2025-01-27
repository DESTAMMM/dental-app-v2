def render_historial_clinico_list(historiales):
    return [
        {
            "id_historial": historial.id_historial,
            "id_paciente": historial.id_paciente,
            "fecha": historial.fecha.strftime('%Y-%m-%d'),
            "diagnostico": historial.diagnostico,
            "tratamiento": historial.tratamiento,
            "observaciones": historial.observaciones
        }
        for historial in historiales
    ]

def render_historial_detail(historial):
    return {
        "id_historial": historial.id_historial,
        "id_paciente": historial.id_paciente,
        "fecha": historial.fecha.strftime('%Y-%m-%d'),
        "diagnostico": historial.diagnostico,
        "tratamiento": historial.tratamiento,
        "observaciones": historial.observaciones
    } 