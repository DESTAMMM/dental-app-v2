from flask import Blueprint, request, jsonify
from models.inventario_model import Inventario
from models.proveedor_model import Proveedor
from models.pedido_model import Pedido
from views.inventario_view import render_inventario_list, render_inventario_detail
from views.proveedor_view import render_proveedores_list, render_proveedor_detail
from views.pedido_view import render_pedidos_list, render_pedido_detail
from utils.decorator import roles_required
from datetime import datetime, timedelta

from sqlalchemy.orm import joinedload


inventario_bp = Blueprint('inventario', __name__)

# Rutas para Inventario

@inventario_bp.route('/inventario', methods=['POST'])
@roles_required('admin', 'asistente')
def create_producto():
    data = request.get_json()
    try:
        # Validar entrada
        if not data.get('nombre_producto') or not data.get('categoria') or not data.get('cantidad'):
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        nuevo_producto = Inventario(
            nombre_producto=data['nombre_producto'],
            categoria=data['categoria'],
            cantidad=data['cantidad'],
            fecha_ingreso=data['fecha_ingreso'],
            fecha_vencimiento=data.get('fecha_vencimiento')
        )
        nuevo_producto.save()
        return jsonify({"message": "Producto creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el producto: {str(e)}"}), 400

@inventario_bp.route('/inventario', methods=['GET'])
@roles_required('admin', 'asistente')
def get_all_productos():
    try:
        productos = Inventario.get_all()
        return jsonify(render_inventario_list(productos)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los productos: {str(e)}"}), 400
    
@inventario_bp.route('/inventario/<int:id_producto>', methods=['GET'])
@roles_required('admin', 'asistente')
def get_producto(id_producto):
    try:
        producto = Inventario.get_by_id(id_producto)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(render_inventario_detail(producto)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el producto: {str(e)}"}), 400

@inventario_bp.route('/inventario/<int:id_producto>', methods=['PUT'])
@roles_required('admin', 'asistente')
def update_producto(id_producto):
    data = request.get_json()
    try:
        producto = Inventario.get_by_id(id_producto)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        producto.update(
            nombre_producto=data.get('nombre_producto'),
            categoria=data.get('categoria'),
            cantidad=data.get('cantidad'),
            fecha_ingreso=data.get('fecha_ingreso'),
            fecha_vencimiento=data.get('fecha_vencimiento')
        )
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 400

@inventario_bp.route('/inventario/<int:id_producto>', methods=['DELETE'])
@roles_required('admin')
def delete_producto(id_producto):
    try:
        producto = Inventario.get_by_id(id_producto)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        # Establecer id_producto en NULL para pedidos relacionados
        if producto.pedidos:
            for pedido in producto.pedidos:
                pedido.id_producto = None
        producto.delete()
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el producto: {str(e)}"}), 400
    
# Rutas para Proveedores

@inventario_bp.route('/proveedores', methods=['POST'])
@roles_required('admin', 'asistente')
def create_proveedor():
    data = request.get_json()
    nuevo_proveedor = Proveedor(
        nombre=data['nombre'],
        direccion=data['direccion'],
        correo_electronico=data['correo_electronico']
    )
    nuevo_proveedor.save()
    return jsonify({"message": "Proveedor creado exitosamente"}), 201

@inventario_bp.route('/proveedores', methods=['GET'])
@roles_required('admin', 'asistente')
def get_all_proveedores():
    try:
        proveedores = Proveedor.get_all()
        return jsonify(render_proveedores_list(proveedores)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los proveedores: {str(e)}"}), 400

@inventario_bp.route('/proveedores/<int:id_proveedor>', methods=['GET'])
@roles_required('admin', 'asistente')
def get_proveedor(id_proveedor):
    try:
        proveedor = Proveedor.get_by_id(id_proveedor)
        if not proveedor:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        return jsonify(render_proveedor_detail(proveedor)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el proveedor: {str(e)}"}), 400

@inventario_bp.route('/proveedores/<int:id_proveedor>', methods=['PUT'])
@roles_required('admin', 'asistente')
def update_proveedor(id_proveedor):
    data = request.get_json()
    try:
        proveedor = Proveedor.get_by_id(id_proveedor)
        if not proveedor:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        proveedor.update(
            nombre=data.get('nombre'),
            direccion=data.get('direccion'),
            correo_electronico=data.get('correo_electronico')
        )
        return jsonify({"message": "Proveedor actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el proveedor: {str(e)}"}), 400

@inventario_bp.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
@roles_required('admin')
def delete_proveedor(id_proveedor):
    try:
        proveedor = Proveedor.get_by_id(id_proveedor)
        if not proveedor:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        # Actualizar pedidos relacionados
        pedidos = Pedido.query.filter_by(id_proveedor=id_proveedor).all()
        for pedido in pedidos:
            pedido.id_proveedor = None  # Establecer id_proveedor en NULL
        proveedor.delete()  # Eliminar el proveedor
        return jsonify({"message": "Proveedor eliminado exitosamente. Los pedidos relacionados han sido actualizados."}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el proveedor: {str(e)}"}), 400


# Rutas para Pedidos

@inventario_bp.route('/pedidos', methods=['POST'])
@roles_required('admin', 'asistente')
def create_pedido():
    data = request.get_json()
    try:
        # Validar entrada
        producto = Inventario.query.filter_by(nombre_producto=data['nombre_producto']).first()
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        proveedor = Proveedor.query.filter_by(nombre=data['nombre_proveedor']).first()
        if not proveedor:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        # Crear el pedido
        nuevo_pedido = Pedido(
            id_producto=producto.id_producto,
            id_proveedor=proveedor.id_proveedor,
            cantidad=data['cantidad'],
            fecha_pedido=data['fecha_pedido'],
            fecha_entrega=data.get('fecha_entrega'),
            estado_pedido=data.get('estado_pedido', 'pendiente')
        )
        nuevo_pedido.save()
        return jsonify({"message": "Pedido creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el pedido: {str(e)}"}), 400
    
@inventario_bp.route('/pedidos', methods=['GET'])
@roles_required('admin', 'asistente')
def get_all_pedidos():
    try:
        pedidos = Pedido.get_all()
        return jsonify(render_pedidos_list(pedidos)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los pedidos: {str(e)}"}), 400

@inventario_bp.route('/pedidos/<int:id_pedido>', methods=['GET'])
@roles_required('admin', 'asistente')
def get_pedido(id_pedido):
    try:
        pedido = Pedido.get_by_id(id_pedido)
        if not pedido:
            return jsonify({"error": "Pedido no encontrado"}), 404
        return jsonify(render_pedido_detail(pedido)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el pedido: {str(e)}"}), 400

@inventario_bp.route('/pedidos/<int:id_pedido>', methods=['PUT'])
@roles_required('admin', 'asistente')
def update_pedido(id_pedido):
    data = request.get_json()
    pedido = Pedido.get_by_id(id_pedido)
    if pedido:
        pedido.update(
            cantidad=data.get('cantidad'),
            fecha_pedido=data.get('fecha_pedido'),
            fecha_entrega=data.get('fecha_entrega'),
            estado_pedido=data.get('estado_pedido')
        )
        return jsonify({"message": "Pedido actualizado exitosamente"}), 200
    return jsonify({"error": "Pedido no encontrado"}), 404

@inventario_bp.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
@roles_required('admin')
def delete_pedido(id_pedido):
    try:
        pedido = Pedido.get_by_id(id_pedido)
        if not pedido:
            return jsonify({"error": "Pedido no encontrado"}), 404

        pedido.delete()
        return jsonify({"message": "Pedido eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el pedido: {str(e)}"}), 400

@inventario_bp.route('/pedidos', methods=['GET'])
@roles_required('admin', 'asistente')
def get_pedidos_por_estado():
    estado = request.args.get('estado')  # Estado como parámetro opcional
    try:
        # Cargar pedidos junto con sus relaciones (producto y proveedor)
        query = Pedido.query.options(
            joinedload(Pedido.producto),
            joinedload(Pedido.proveedor)
        )
        # Filtrar por estado si se proporciona
        if estado:
            pedidos = query.filter(Pedido.estado == estado).all()
            if not pedidos:
                return jsonify({"message": f"No se encontraron pedidos con estado '{estado}'"}), 404
        else:
            pedidos = query.all()
            if not pedidos:
                return jsonify({"message": "No hay pedidos registrados"}), 404

        # Renderizar la lista de pedidos usando la vista
        return jsonify(render_pedidos_list(pedidos)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los pedidos: {str(e)}"}), 400

@inventario_bp.route('/inventario/productos_vencimiento', methods=['GET'])
@roles_required('admin', 'asistente')
def get_productos_vencimiento():
    try:
        # Validar parámetros de entrada
        dias = int(request.args.get('dias', default=30))
        categoria = request.args.get('categoria')
        # Calcular la fecha límite
        fecha_limite = datetime.now() + timedelta(days=dias)
        # Filtrar productos próximos a vencer según la categoría
        if categoria:
            productos = Inventario.query.filter(
                Inventario.categoria == categoria,
                Inventario.fecha_vencimiento <= fecha_limite
            ).all()
        else:
            productos = Inventario.query.filter(
                Inventario.fecha_vencimiento <= fecha_limite
            ).all()
        # Validar si no se encontraron productos
        if not productos:
            return jsonify({"message": "No se encontraron productos próximos a vencer"}), 404
        # Renderizar la lista de productos con la vista
        return jsonify(render_inventario_list(productos)), 200
    except ValueError:
        return jsonify({"error": "El parámetro 'dias' debe ser un número entero válido"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al obtener productos próximos a vencer: {str(e)}"}), 400
