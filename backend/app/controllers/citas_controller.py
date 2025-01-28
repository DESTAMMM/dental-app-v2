from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt
from models.usuario_model import Usuario
from models.paciente_model import Paciente
from models.doctor_model import Doctor
from models.citas_model import Cita
from utils.decorator import roles_required
from views.citas_view import render_citas_list, render_cita_detail
from sqlalchemy.orm import joinedload

citas_bp = Blueprint('citas', __name__)

# Crear una nueva cita
@citas_bp.route('/citas', methods=['POST'])
@roles_required('admin', 'asistant')
def create_cita():
    data = request.get_json()
    try:
        # Validar entrada
        fecha_str = data.get('fecha_cita')  # Fecha en formato 'YYYY-MM-DD'
        hora_str = data.get('hora_cita')    # Hora en formato 'HH:MM:SS'
        if not fecha_str or not hora_str:
            return jsonify({"error": "Los campos 'fecha_cita' y 'hora_cita' son obligatorios"}), 400
        try:
            # Convertir fecha y hora a los formatos correspondientes
            fecha_cita = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_cita = datetime.strptime(hora_str, '%H:%M:%S').time()
        except ValueError:
            return jsonify({"error": "El formato de 'fecha_cita' debe ser 'YYYY-MM-DD' y 'hora_cita' debe ser 'HH:MM:SS'"}), 400
        nueva_cita = Cita(
            id_paciente=data['id_paciente'],
            id_doctor=data['id_doctor'],
            fecha_cita=fecha_cita,
            hora_cita=hora_cita,
            motivo_cita=data['motivo_cita'],
            estado=data.get('estado', 'pendiente')
        )
        nueva_cita.save()
        return jsonify({"message": "Cita creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear la cita: {str(e)}"}), 400

# Obtener todas las citas
@citas_bp.route('/citas', methods=['GET'])
@roles_required('admin', 'asistant')
def get_all_citas():
    try:
        citas = Cita.query.options(
            joinedload(Cita.paciente).joinedload(Paciente.usuario),  
            joinedload(Cita.doctor).joinedload(Doctor.usuario)
        ).all()
        return jsonify(render_citas_list(citas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las citas: {str(e)}"}), 400

# Obtener citas del paciente autenticado
@citas_bp.route('/mis_citas', methods=['GET'])
@roles_required('paciente')
def get_mis_citas():
    try:
        # Obtener claims del token JWT
        claims = get_jwt()
        id_paciente = claims.get("id_especializacion")  # ID del paciente desde el token
        # Validar que el token tenga el ID del paciente
        if not id_paciente:
            return jsonify({"error": "No se encontró información del paciente en el token"}), 400
        # Consultar citas asociadas al paciente
        citas = Cita.query.filter_by(id_paciente=id_paciente).all()
        if not citas:
            return jsonify({"message": "No se encontraron citas para este paciente"}), 404
        # Renderizar la lista de citas
        return jsonify(render_citas_list(citas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener tus citas: {str(e)}"}), 500
    
@citas_bp.route('/citas/filtrar', methods=['GET'])
@roles_required('admin', 'asistant')
def filtrar_citas():
    try:
        # Obtener parámetros
        nombre_paciente = request.args.get('nombre_paciente')
        nombre_doctor = request.args.get('nombre_doctor')
        fecha_str = request.args.get('fecha_cita')  # Formato 'YYYY-MM-DD'
        # Construir la consulta base
        query = Cita.query
        # Filtrar por nombre del paciente
        if nombre_paciente:
            query = query.join(Cita.paciente).join(Paciente.usuario).filter(
                Usuario.nombre.ilike(f"%{nombre_paciente}%")
            )
        # Filtrar por nombre del doctor
        if nombre_doctor:
            query = query.join(Cita.doctor).join(Doctor.usuario).filter(
                Usuario.nombre.ilike(f"%{nombre_doctor}%")
            )
        # Filtrar por fecha_cita
        if fecha_str:
            try:
                fecha_cita = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                query = query.filter(Cita.fecha_cita == fecha_cita)
            except ValueError:
                return jsonify({"error": "El formato de 'fecha_cita' debe ser 'YYYY-MM-DD'"}), 400
        # Ejecutar la consulta
        citas = query.options(
            joinedload(Cita.paciente).joinedload(Paciente.usuario),
            joinedload(Cita.doctor).joinedload(Doctor.usuario)
        ).all()
        return jsonify(render_citas_list(citas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al filtrar las citas: {str(e)}"}), 400

# Actualizar una cita
@citas_bp.route('/citas/<int:id_cita>', methods=['PUT'])
@roles_required('admin', 'asistant')
def update_cita(id_cita):
    data = request.get_json()
    try:
        cita = Cita.get_by_id(id_cita)
        if not cita:
            return jsonify({"error": "Cita no encontrada"}), 404
        # Validar y convertir fecha_cita y hora_cita si se proporcionan
        fecha_str = data.get('fecha_cita')
        hora_str = data.get('hora_cita')
        if fecha_str:
            try:
                data['fecha_cita'] = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "El formato de 'fecha_cita' debe ser 'YYYY-MM-DD'"}), 400
        if hora_str:
            try:
                data['hora_cita'] = datetime.strptime(hora_str, '%H:%M:%S').time()
            except ValueError:
                return jsonify({"error": "El formato de 'hora_cita' debe ser 'HH:MM:SS'"}), 400
        # Actualizar la cita con los datos proporcionados
        cita.update(
            id_doctor=data.get('id_doctor'),
            fecha_cita=data.get('fecha_cita'),
            hora_cita=data.get('hora_cita'),
            motivo_cita=data.get('motivo_cita'),
            estado=data.get('estado')
        )
        return jsonify({"message": "Cita actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la cita: {str(e)}"}), 400

# Eliminar una cita
@citas_bp.route('/citas/<int:id_cita>', methods=['DELETE'])
@roles_required('admin')
def delete_cita(id_cita):
    try:
        cita = Cita.get_by_id(id_cita)
        if not cita:
            return jsonify({"error": "Cita no encontrada"}), 404
        cita.delete()
        return jsonify({"message": "Cita eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la cita: {str(e)}"}), 400

#6