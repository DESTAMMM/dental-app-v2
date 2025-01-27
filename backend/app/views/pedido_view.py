def render_pedidos_list(pedidos):
    return [
        {
            "id_pedido": pedido.id,
            "id_producto": pedido.producto_id,
            "nombre_producto": pedido.producto.nombre if pedido.producto else None,
            "id_proveedor": pedido.proveedor_id,
            "nombre_proveedor": pedido.proveedor.nombre if pedido.proveedor else None,
            "cantidad": pedido.cantidad,
            "fecha_pedido": pedido.fecha_pedido.strftime('%Y-%m-%d') if pedido.fecha_pedido else None,
            "fecha_entrega": pedido.fecha_entrega.strftime('%Y-%m-%d') if pedido.fecha_entrega else None,
            "estado_pedido": pedido.estado
        }
        for pedido in pedidos
    ]
def render_pedido_detail(pedido):
    return {
        "id_pedido": pedido.id,
        "id_producto": pedido.producto_id,
        "nombre_producto": pedido.producto.nombre if pedido.producto else None,
        "id_proveedor": pedido.proveedor_id,
        "nombre_proveedor": pedido.proveedor.nombre if pedido.proveedor else None,
        "cantidad": pedido.cantidad,
        "fecha_pedido": pedido.fecha_pedido.strftime('%Y-%m-%d') if pedido.fecha_pedido else None,
        "fecha_entrega": pedido.fecha_entrega.strftime('%Y-%m-%d') if pedido.fecha_entrega else None,
        "estado_pedido": pedido.estado
    }