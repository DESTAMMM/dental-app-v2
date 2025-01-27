def render_factura_list(facturas):
    return [
        {
            "id_factura": factura.id_factura,
            "fecha_factura": factura.fecha_factura.strftime("%Y-%m-%d"),
            "monto_total": factura.monto_total,
            "estado_pago": factura.estado_pago,
            "paciente": {
                "id_paciente": factura.paciente.id_paciente,
                "nombre": factura.paciente.usuario.nombre,
                "apellido": factura.paciente.usuario.apellido,
            },
        }
        for factura in facturas
    ]
def render_factura_detail(factura):
    return {
        "id_factura": factura.id_factura,
        "fecha_factura": factura.fecha_factura.strftime("%Y-%m-%d"),
        "monto_total": factura.monto_total,
        "estado_pago": factura.estado_pago,
        "paciente": {
            "id_paciente": factura.paciente.id_paciente,
            "nombre": factura.paciente.usuario.nombre,
            "apellido": factura.paciente.usuario.apellido,
        },
        "detalles": [
            {
                "id_detalle": detalle.id_detalle,
                "descripcion_tratamiento": detalle.descripcion_tratamiento,
                "costo": detalle.costo,
                "fecha_tratamiento": detalle.fecha_tratamiento.strftime("%Y-%m-%d"),
                "doctor": {
                    "nombre": detalle.doctor.usuario.nombre,
                    "apellido": detalle.doctor.usuario.apellido,
                },
            }
            for detalle in factura.detalles
        ],
    }