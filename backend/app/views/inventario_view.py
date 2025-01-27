def render_inventario_list(productos):
    return [
        {
            "id_producto": producto.id_producto,
            "nombre_producto": producto.nombre_producto,
            "categoria": producto.categoria,
            "cantidad": producto.cantidad,
            "fecha_ingreso": producto.fecha_ingreso,
            "fecha_vencimiento": producto.fecha_vencimiento,
        }
        for producto in productos
    ]

def render_inventario_detail(producto):
    return {
        "id_producto": producto.id_producto,
        "nombre_producto": producto.nombre_producto,
        "categoria": producto.categoria,
        "cantidad": producto.cantidad,
        "fecha_ingreso": producto.fecha_ingreso,
        "fecha_vencimiento": producto.fecha_vencimiento,
    }