from flask import Blueprint, request, jsonify
from models.factura_model import Factura
from models.detalle_factura_model import DetalleFactura
from models.paciente_model import Paciente
from models.doctor_model import Doctor
from views.factura_view import render_factura_list, render_factura_detail
from flask_jwt_extended import get_jwt_identity
from utils.decorator import roles_required
from sqlalchemy.orm import joinedload

facturas_bp = Blueprint("facturas", __name__)

# Crear una factura
@facturas_bp.route("/facturas", methods=["POST"])
@roles_required("admin", "asistant")
def create_factura():
    data = request.get_json()
    try:
        nueva_factura = Factura(
            id_paciente=data["id_paciente"],
            fecha_factura=data["fecha_factura"],
            monto_total=data["monto_total"],
            estado_pago=data["estado_pago"],
        )
        nueva_factura.save()
        return jsonify({"message": "Factura creada exitosamente"}), 201
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
            db.joinedload(Factura.detalles).joinedload(DetalleFactura.doctor).joinedload(Doctor.usuario),
            db.joinedload(Factura.paciente).joinedload(Paciente.usuario)
        ).all()

        return jsonify(render_factura_list(facturas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las facturas: {str(e)}"}), 400

# Obtener detalles de una factura específica
@facturas_bp.route("/facturas/<int:id_factura>", methods=["GET"])
@roles_required("admin", "asistant", "usuario")
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

# Ver facturas del usuario actual (paciente)
@facturas_bp.route("/facturas/mis_facturas", methods=["GET"])
@roles_required("usuario")
def get_my_facturas():
    try:
        current_user_id = get_jwt_identity()
        facturas = Factura.query.filter(Factura.id_paciente == current_user_id).all()
        return jsonify(render_factura_list(facturas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las facturas del usuario: {str(e)}"}), 400

# Filtrar facturas
@facturas_bp.route("/facturas/filtrar", methods=["GET"])
@roles_required("admin", "asistant")
def filtrar_facturas():
    try:
        nombre_paciente = request.args.get("nombre_paciente")
        nombre_doctor = request.args.get("nombre_doctor")
        fecha = request.args.get("fecha")  # Formato YYYY-MM-DD
        query = Factura.query
        if nombre_paciente:
            query = query.join(Factura.paciente).join(Paciente.usuario).filter(
                Usuario.nombre.ilike(f"%{nombre_paciente}%")
            )
        if nombre_doctor:
            query = query.join(Factura.detalles).join(DetalleFactura.doctor).join(Doctor.usuario).filter(
                Usuario.nombre.ilike(f"%{nombre_doctor}%")
            )
        if fecha:
            query = query.filter(Factura.fecha_factura.cast(db.Date) == fecha)
        facturas = query.all()
        return jsonify(render_factura_list(facturas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al filtrar las facturas: {str(e)}"}), 400
