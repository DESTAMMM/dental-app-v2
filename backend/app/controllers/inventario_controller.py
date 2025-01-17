from flask import Blueprint, request, jsonify
from models.inventario_model import Inventario
from models.proveedor_model import Proveedor
from models.pedido_model import Pedido
from utils.decorator import roles_required
from database import db

from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

inventario_bp = Blueprint('inventario', __name__)

# Rutas para Inventario

@inventario_bp.route('/inventario', methods=['POST'])
@roles_required('admin', 'asistente')
def create_producto():
    data = request.get_json()
    nuevo_producto = Inventario(
        nombre_producto=data['nombre_producto'],
        categoria=data['categoria'],
        cantidad=data['cantidad'],
        fecha_ingreso=data['fecha_ingreso'],
        fecha_vencimiento=data.get('fecha_vencimiento')
    )
    nuevo_producto.save()
    return jsonify({"message": "Producto creado exitosamente"}), 201

@inventario_bp.route('/inventario', methods=['GET'])
@roles_required('admin', 'asistente', 'usuario')
def get_all_productos():
    productos = Inventario.get_all()
    productos_list = [{"id_producto": producto.id_producto, "nombre_producto": producto.nombre_producto, "categoria": producto.categoria, "cantidad": producto.cantidad, "fecha_ingreso": producto.fecha_ingreso, "fecha_vencimiento": producto.fecha_vencimiento} for producto in productos]
    return jsonify(productos_list), 200

@inventario_bp.route('/inventario/<int:id_producto>', methods=['GET'])
@roles_required('admin', 'asistente', 'usuario')
def get_producto(id_producto):
    producto = Inventario.get_by_id(id_producto)
    if producto:
        return jsonify({
            "id_producto": producto.id_producto,
            "nombre_producto": producto.nombre_producto,
            "categoria": producto.categoria,
            "cantidad": producto.cantidad,
            "fecha_ingreso": producto.fecha_ingreso,
            "fecha_vencimiento": producto.fecha_vencimiento
        }), 200
    return jsonify({"error": "Producto no encontrado"}), 404

@inventario_bp.route('/inventario/<int:id_producto>', methods=['PUT'])
@roles_required('admin', 'asistente')
def update_producto(id_producto):
    data = request.get_json()
    producto = Inventario.get_by_id(id_producto)
    if producto:
        producto.update(
            nombre_producto=data.get('nombre_producto'),
            categoria=data.get('categoria'),
            cantidad=data.get('cantidad'),
            fecha_ingreso=data.get('fecha_ingreso'),
            fecha_vencimiento=data.get('fecha_vencimiento')
        )
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    return jsonify({"error": "Producto no encontrado"}), 404

@inventario_bp.route('/inventario/<int:id_producto>', methods=['DELETE'])
@roles_required('admin')
def delete_producto(id_producto):
    producto = Inventario.get_by_id(id_producto)
    if producto:
        producto.delete()
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    return jsonify({"error": "Producto no encontrado"}), 404


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
@roles_required('admin', 'asistente', 'usuario')
def get_all_proveedores():
    proveedores = Proveedor.get_all()
    proveedores_list = [{"id_proveedor": proveedor.id_proveedor, "nombre": proveedor.nombre, "direccion": proveedor.direccion, "correo_electronico": proveedor.correo_electronico} for proveedor in proveedores]
    return jsonify(proveedores_list), 200

@inventario_bp.route('/proveedores/<int:id_proveedor>', methods=['GET'])
@roles_required('admin', 'asistente', 'usuario')
def get_proveedor(id_proveedor):
    proveedor = Proveedor.get_by_id(id_proveedor)
    if proveedor:
        return jsonify({
            "id_proveedor": proveedor.id_proveedor,
            "nombre": proveedor.nombre,
            "direccion": proveedor.direccion,
            "correo_electronico": proveedor.correo_electronico
        }), 200
    return jsonify({"error": "Proveedor no encontrado"}), 404

@inventario_bp.route('/proveedores/<int:id_proveedor>', methods=['PUT'])
@roles_required('admin', 'asistente')
def update_proveedor(id_proveedor):
    data = request.get_json()
    proveedor = Proveedor.get_by_id(id_proveedor)
    if proveedor:
        proveedor.update(
            nombre=data.get('nombre'),
            direccion=data.get('direccion'),
            correo_electronico=data.get('correo_electronico')
        )
        return jsonify({"message": "Proveedor actualizado exitosamente"}), 200
    return jsonify({"error": "Proveedor no encontrado"}), 404

@inventario_bp.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
@roles_required('admin')
def delete_proveedor(id_proveedor):
    proveedor = Proveedor.get_by_id(id_proveedor)
    if proveedor:
        proveedor.delete()
        return jsonify({"message": "Proveedor eliminado exitosamente"}), 200
    return jsonify({"error": "Proveedor no encontrado"}), 404


# Rutas para Pedidos

@inventario_bp.route('/pedidos', methods=['POST']) 
@roles_required('admin', 'asistente') 
def create_pedido(): 
    data = request.get_json()
    # Convertir nombres a IDs 
    producto = Inventario.query.filter_by(nombre_producto=data['nombre_producto']).first() 
    if not producto: 
        return jsonify({"error": "Producto no encontrado"}), 404 
    proveedor = Proveedor.query.filter_by(nombre=data['nombre_proveedor']).first() 
    if not proveedor: 
        return jsonify({"error": "Proveedor no encontrado"}), 404 
    nuevo_pedido = Pedido( id_producto=producto.id_producto, 
                        id_proveedor=proveedor.id_proveedor, 
                        cantidad=data['cantidad'], 
                        fecha_pedido=data['fecha_pedido'], 
                        fecha_entrega=data.get('fecha_entrega'), 
                        estado_pedido=data.get('estado_pedido', 'pendiente') 
                        ) 
    nuevo_pedido.save() 
    return jsonify({"message": "Pedido creado exitosamente"}), 201

@inventario_bp.route('/pedidos', methods=['GET'])
@roles_required('admin', 'asistente')
def get_all_pedidos():
    pedidos = Pedido.get_all()
    pedidos_list = [{"id_pedido": pedido.id_pedido, 
                     "id_producto": pedido.id_producto, 
                     "id_proveedor": pedido.id_proveedor, 
                     "cantidad": pedido.cantidad, 
                     "fecha_pedido": pedido.fecha_pedido, 
                     "fecha_entrega": pedido.fecha_entrega, 
                     "estado_pedido": pedido.estado_pedido
                     } 
                     for pedido in pedidos]
    return jsonify(pedidos_list), 200

@inventario_bp.route('/pedidos/<int:id_pedido>', methods=['GET'])
@roles_required('admin', 'asistente')
def get_pedido(id_pedido):
    pedido = Pedido.get_by_id(id_pedido)
    if pedido:
        return jsonify({
            "id_pedido": pedido.id_pedido,
            "id_producto": pedido.id_producto,
            "id_proveedor": pedido.id_proveedor,
            "cantidad": pedido.cantidad,
            "fecha_pedido": pedido.fecha_pedido,
            "fecha_entrega": pedido.fecha_entrega,
            "estado_pedido": pedido.estado_pedido
        }), 200
    return jsonify({"error": "Pedido no encontrado"}), 404

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
    pedido = Pedido.get_by_id(id_pedido)
    if pedido:
        pedido.delete()
        return jsonify({"message": "Pedido eliminado exitosamente"}), 200
    return jsonify({"error": "Pedido no encontrado"}), 404

@inventario_bp.route('/pedidos_pendientes', methods=['GET'])
@roles_required('admin', 'asistente')
def get_pedidos_pendientes():
    pedidos = Pedido.query.options(
        joinedload(Pedido.producto),
        joinedload(Pedido.proveedor)
    ).filter(Pedido.estado_pedido == 'pendiente').all()

    pedidos_list = [
        {
            "id_pedido": pedido.id_pedido,
            "producto": {
                "id_producto": pedido.producto.id_producto,
                "nombre_producto": pedido.producto.nombre_producto,
                "categoria": pedido.producto.categoria
            },
            "proveedor": {
                "id_proveedor": pedido.proveedor.id_proveedor,
                "nombre": pedido.proveedor.nombre
            },
            "cantidad": pedido.cantidad,
            "fecha_pedido": pedido.fecha_pedido,
            "fecha_entrega": pedido.fecha_entrega,
            "estado_pedido": pedido.estado_pedido
        } for pedido in pedidos
    ]

    return jsonify(pedidos_list), 200


@inventario_bp.route('/inventario/productos_vencimiento', methods=['GET']) 
@roles_required('admin', 'asistente') 
def get_productos_vencimiento(): 
    categoria = request.args.get('categoria')
    dias = int(request.args.get('dias', default=30)) 
    fecha_limite = datetime.now() + timedelta(days=dias) 
    # Consulta para obtener productos próximos a vencer 
    if categoria: productos = Inventario.query.filter( 
        Inventario.categoria == categoria, 
        Inventario.fecha_vencimiento <= fecha_limite ).all() 
    else: productos = Inventario.query.filter( 
        Inventario.fecha_vencimiento <= fecha_limite ).all() 
    # Crear una lista de productos con información adicional 
    productos_list = [ { "id_producto": producto.id_producto, 
                        "nombre_producto": producto.nombre_producto, 
                        "categoria": producto.categoria, "cantidad": producto.cantidad, 
                        "fecha_ingreso": producto.fecha_ingreso, "fecha_vencimiento": producto.fecha_vencimiento 
                        } for producto in productos ] 
    return jsonify(productos_list), 200