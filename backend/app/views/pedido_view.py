def render_pedidos_list(pedidos):
    return [
        {
            "id_pedido": pedido.id,
            "id_producto": pedido.producto_id,
            "nombre_producto": pedido.producto.nombre,
            "id_proveedor": pedido.proveedor_id,
            "nombre_proveedor": pedido.proveedor.nombre,
            "cantidad": pedido.cantidad,
            "fecha_pedido": pedido.fecha_pedido,
            "fecha_entrega": pedido.fecha_entrega,
            "estado_pedido": pedido.estado
        }
        for pedido in pedidos
    ]

def render_pedido_detail(pedido):
    return {
        "id_pedido": pedido.id,
        "id_producto": pedido.producto_id,
        "nombre_producto": pedido.producto.nombre,
        "id_proveedor": pedido.proveedor_id,
        "nombre_proveedor": pedido.proveedor.nombre,
        "cantidad": pedido.cantidad,
        "fecha_pedido": pedido.fecha_pedido,
        "fecha_entrega": pedido.fecha_entrega,
        "estado_pedido": pedido.estado
    }