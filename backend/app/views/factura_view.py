def render_facturas_list(facturas):
    return [
        {
            "id": factura.id,
            "fecha": factura.fecha_factura,
            "monto_total": factura.monto_total,
            "estado_pago": factura.estado_pago,
            "usuario_id": factura.usuario_id,
        }
        for factura in facturas
    ]

def render_factura_detail(factura):
    return {
        "id": factura.id,
        "fecha": factura.fecha_factura,
        "monto_total": factura.monto_total,
        "estado_pago": factura.estado_pago,
        "usuario_id": factura.usuario_id,
    }