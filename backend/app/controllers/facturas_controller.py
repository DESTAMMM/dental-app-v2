from datetime import datetime
from flask import Blueprint, request, jsonify
from models.factura_model import Factura
from database import db
from models.detalle_factura_model import DetalleFactura
from models.paciente_model import Paciente
from models.doctor_model import Doctor
from models.usuario_model import Usuario
from views.factura_view import render_factura_list, render_factura_detail
from flask_jwt_extended import  get_jwt
from utils.decorator import roles_required
from sqlalchemy.orm import joinedload

facturas_bp = Blueprint("facturas", __name__)

@facturas_bp.route('/facturas', methods=['POST'])
@roles_required('admin', 'asistant')
def create_factura():
    data = request.get_json()
    try:
        # Validar datos básicos de la factura
        id_paciente = data.get('id_paciente')
        fecha_factura = data.get('fecha_factura')
        monto_total = data.get('monto_total')
        estado_pago = data.get('estado_pago')
        detalles = data.get('detalles', [])  # Detalles de factura (array)
        if not id_paciente or not fecha_factura or not monto_total or not estado_pago:
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        # Crear la factura
        nueva_factura = Factura(
            id_paciente=id_paciente,
            fecha_factura=fecha_factura,
            monto_total=monto_total,
            estado_pago=estado_pago
        )
        nueva_factura.save()
        # Crear los detalles de factura si existen
        if not detalles:
            return jsonify({"error": "Debe incluir al menos un detalle de factura"}), 400
        for detalle in detalles:
            nuevo_detalle = DetalleFactura(
                id_factura=nueva_factura.id_factura,
                descripcion_tratamiento=detalle.get('descripcion_tratamiento'),
                costo=detalle.get('costo'),
                id_doctor=detalle.get('id_doctor'),
                fecha_tratamiento=detalle.get('fecha_tratamiento')
            )
            nuevo_detalle.save()
        return jsonify({"message": "Factura y detalles creados exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear la factura: {str(e)}"}), 400
# Crear detalle factura
@facturas_bp.route("/detalle_factura", methods=["POST"])
@roles_required("admin", "asistant")
def create_detalle_factura():
    data = request.get_json()
    try:
        # Crear un nuevo detalle de factura
        nuevo_detalle = DetalleFactura(
            id_factura=data["id_factura"],
            descripcion_tratamiento=data["descripcion_tratamiento"],
            costo=data["costo"],
            id_doctor=data["id_doctor"],
            fecha_tratamiento=data["fecha_tratamiento"],
        )
        nuevo_detalle.save()
        return jsonify({"message": "Detalle de factura creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el detalle de factura: {str(e)}"}), 400

@facturas_bp.route("/facturas", methods=["GET"])
@roles_required("admin", "asistant")
def get_all_facturas():
    try:
        # Obtener todas las facturas junto con sus detalles
        facturas = Factura.query.options(
            joinedload(Factura.detalles).joinedload(DetalleFactura.doctor).joinedload(Doctor.usuario),
            joinedload(Factura.paciente).joinedload(Paciente.usuario)
        ).all()

        return jsonify(render_factura_list(facturas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las facturas: {str(e)}"}), 400

# Obtener detalles de una factura específica
@facturas_bp.route("/facturas/<int:id_factura>", methods=["GET"])
@roles_required("admin", "asistant", "paciente")
def get_factura_details(id_factura):
    try:
        factura = Factura.get_by_id(id_factura)
        if not factura:
            return jsonify({"error": "Factura no encontrada"}), 404
        return jsonify(render_factura_detail(factura)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los detalles de la factura: {str(e)}"}), 400

# Actualizar una factura
@facturas_bp.route("/facturas/<int:id_factura>", methods=["PUT"])
@roles_required("admin", "asistant")
def update_factura(id_factura):
    data = request.get_json()
    try:
        factura = Factura.get_by_id(id_factura)
        if not factura:
            return jsonify({"error": "Factura no encontrada"}), 404
        factura.update(
            fecha_factura=data.get("fecha_factura"),
            monto_total=data.get("monto_total"),
            estado_pago=data.get("estado_pago"),
        )
        return jsonify({"message": "Factura actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la factura: {str(e)}"}), 400

@facturas_bp.route("/detalle_factura/<int:id_detalle>", methods=["PUT"])
@roles_required("admin", "asistant")
def update_detalle_factura(id_detalle):
    data = request.get_json()
    try:
        detalle = DetalleFactura.get_by_id(id_detalle)
        if not detalle:
            return jsonify({"error": "Detalle de factura no encontrado"}), 404

        # Actualizar los campos del detalle
        detalle.update(
            descripcion_tratamiento=data.get("descripcion_tratamiento"),
            costo=data.get("costo"),
            fecha_tratamiento=data.get("fecha_tratamiento"),
        )
        return jsonify({"message": "Detalle de factura actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el detalle de factura: {str(e)}"}), 400

# Eliminar una factura
@facturas_bp.route("/facturas/<int:id_factura>", methods=["DELETE"])
@roles_required("admin", "asistant")
def delete_factura(id_factura):
    try:
        factura = Factura.get_by_id(id_factura)
        if not factura:
            return jsonify({"error": "Factura no encontrada"}), 404
        factura.delete()
        return jsonify({"message": "Factura eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la factura: {str(e)}"}), 400

@facturas_bp.route("/detalle_factura/<int:id_detalle>", methods=["DELETE"])
@roles_required("admin", "asistant")
def delete_detalle_factura(id_detalle):
    try:
        detalle = DetalleFactura.get_by_id(id_detalle)
        if not detalle:
            return jsonify({"error": "Detalle de factura no encontrado"}), 404

        # Eliminar el detalle
        detalle.delete()
        return jsonify({"message": "Detalle de factura eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el detalle de factura: {str(e)}"}), 400

@facturas_bp.route('/facturas/mis_facturas', methods=['GET'])
@roles_required('paciente')
def get_my_facturas():
    try:
        # Obtener claims del token JWT
        claims = get_jwt()
        id_paciente = claims.get("id_especializacion")  # ID del paciente desde el token
        # Validar que el paciente tiene un ID válido
        if not id_paciente:
            return jsonify({"error": "No se encontró información del paciente en el token"}), 400
        # Consultar facturas del paciente
        facturas = Factura.query.filter_by(id_paciente=id_paciente).all()
        if not facturas:
            return jsonify({"message": "No se encontraron facturas para este usuario"}), 404
        # Renderizar la lista de facturas
        return jsonify(render_factura_list(facturas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las facturas: {str(e)}"}), 500

# Filtrar facturas
@facturas_bp.route('/facturas/filtrar', methods=['GET'])
@roles_required('admin', 'asistant')
def filtrar_facturas():
    nombre_paciente = request.args.get('nombre_paciente')
    nombre_doctor = request.args.get('nombre_doctor')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    try:
        # Validar formato de fecha si se proporcionan
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        # Construir la consulta de filtrado
        query = Factura.query
        if nombre_paciente:
            query = query.join(Paciente).join(Usuario).filter(
                Usuario.nombre.ilike(f"%{nombre_paciente}%") | Usuario.apellido.ilike(f"%{nombre_paciente}%")
            )
        if nombre_doctor:
            query = query.join(DetalleFactura).join(Doctor).join(Usuario).filter(
                Usuario.nombre.ilike(f"%{nombre_doctor}%") | Usuario.apellido.ilike(f"%{nombre_doctor}%")
            )
        if fecha_inicio and fecha_fin:
            # Si ambas fechas están presentes
            query = query.filter(Factura.fecha_factura.between(fecha_inicio, fecha_fin))
        elif fecha_inicio:
            # Si solo se proporciona fecha de inicio
            query = query.filter(Factura.fecha_factura == fecha_inicio)
        elif fecha_fin:
            # Si solo se proporciona fecha de fin
            query = query.filter(Factura.fecha_factura == fecha_fin)
        facturas = query.all()
        if not facturas:
            return jsonify({"message": "No se encontraron facturas con los filtros proporcionados"}), 404
        return jsonify(render_factura_list(facturas)), 200
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use 'YYYY-MM-DD'"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al filtrar facturas: {str(e)}"}), 400
