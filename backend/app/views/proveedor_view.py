def render_proveedores_list(proveedores):
    return [
        {
            "id_proveedor": proveedor.id,
            "nombre_proveedor": proveedor.nombre,
            "contacto": proveedor.contacto,
            "direccion": proveedor.direccion,
            "productos_proveidos": [producto.id for producto in proveedor.productos]
        }
        for proveedor in proveedores
    ]

def render_proveedor_detail(proveedor):
    return {
        "id_proveedor": proveedor.id,
        "nombre_proveedor": proveedor.nombre,
        "contacto": proveedor.contacto,
        "direccion": proveedor.direccion,
        "productos_proveidos": [producto.id for producto in proveedor.productos]
    }