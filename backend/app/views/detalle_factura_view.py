def render_factura_detalle_list(detalles):
    return [
        {
            "id_detalle": detalle.id,
            "id_factura": detalle.factura_id,
            "descripcion_tratamiento": detalle.descripcion_tratamiento,
            "costo": detalle.costo,
            "id_doctor": detalle.doctor_id,
            "fecha_tratamiento": detalle.fecha_tratamiento
        }
        for detalle in detalles
    ]

def render_factura_detalle_detail(detalle):
    return {
        "id_detalle": detalle.id,
        "id_factura": detalle.factura_id,
        "descripcion_tratamiento": detalle.descripcion_tratamiento,
        "costo": detalle.costo,
        "id_doctor": detalle.doctor_id,
        "fecha_tratamiento": detalle.fecha_tratamiento
    }