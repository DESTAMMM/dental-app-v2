from flask import Blueprint, request, jsonify
from models.historial_clinico_model import HistorialClinico
from models.paciente_model import Paciente
from models.usuario_model import Usuario
from views.historial_clinico_view import render_historial_clinico_list, render_historial_detail
from utils.decorator import roles_required
from flask_jwt_extended import get_jwt

historial_bp = Blueprint('historial', __name__)

# Crear un nuevo historial clínico
@historial_bp.route('/historial', methods=['POST'])
@roles_required('admin', 'asistant')
def create_historial():
    data = request.get_json()
    id_paciente = data.get('id_paciente')
    nombre_paciente = data.get('nombre_paciente')

    if not id_paciente or not nombre_paciente:
        return jsonify({"error": "Los campos 'id_paciente' y 'nombre_paciente' son obligatorios"}), 400
    try:
        # Validar que el paciente existe y el nombre coincide
        paciente = Paciente.get_by_id_and_nombre(id_paciente, nombre_paciente)
        if not paciente:
            return jsonify({"error": "El paciente no existe o el nombre no coincide"}), 404
        # Crear el historial clínico
        nuevo_historial = HistorialClinico(
            id_paciente=id_paciente,
            fecha=data.get('fecha'),
            diagnostico=data.get('diagnostico'),
            tratamiento=data.get('tratamiento'),
            observaciones=data.get('observaciones')
        )
        nuevo_historial.save()

        return jsonify({"message": "Historial clínico creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el historial clínico: {str(e)}"}), 400

@historial_bp.route('/mi_historial', methods=['GET'])
@roles_required('paciente')  # Solo pacientes pueden acceder
def get_mi_historial():
    try:
        # Obtener claims del token JWT
        claims = get_jwt()
        id_paciente = claims.get("id_especializacion")  # ID del paciente desde el token
        # Validar que el ID del paciente esté presente en el token
        if not id_paciente:
            return jsonify({"error": "No se encontró información del paciente en el token"}), 400
        # Obtener los historiales médicos asociados al paciente
        historiales = HistorialClinico.query.filter_by(id_paciente=id_paciente).all()
        if not historiales:
            return jsonify({"message": "No se encontraron historiales médicos"}), 404
        # Renderizar la lista de historiales médicos
        return jsonify(render_historial_clinico_list(historiales)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el historial médico: {str(e)}"}), 500
    
@historial_bp.route('/historial/paciente', methods=['GET'])
@roles_required('admin', 'asistant')
def get_historiales_by_nombre_paciente():
    texto = request.args.get('texto')
    if not texto:
        return jsonify({"error": "El parámetro 'texto' es obligatorio"}), 400
    try:
        # Buscar usuarios cuyos nombres o apellidos coincidan con el texto
        usuarios = Usuario.get_by_nombre_o_apellido(texto)
        if not usuarios:
            return jsonify({"error": "No se encontraron usuarios con ese nombre o apellido"}), 404       
        # Obtener IDs de pacientes asociados
        ids_pacientes = [usuario.paciente.id_paciente for usuario in usuarios if usuario.paciente]

        if not ids_pacientes:
            return jsonify({"error": "No se encontraron pacientes con ese nombre o apellido"}), 404
        
        historiales = HistorialClinico.get_by_pacientes(ids_pacientes)

        if not historiales:
            return jsonify({"message": "No se encontraron historiales clínicos para los pacientes buscados"}), 404

        return jsonify(render_historial_clinico_list(historiales)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los historiales clínicos: {str(e)}"}), 400
    
# Buscar historiales clínicos por rango de fechas
@historial_bp.route('/historial/fechas', methods=['GET'])
@roles_required('admin', 'asistant')
def get_historiales_by_fechas():
    fecha_inicio = request.args.get('fecha_inicio')  # Fecha inicial desde query param
    fecha_fin = request.args.get('fecha_fin')        # Fecha final desde query param

    if not fecha_inicio or not fecha_fin:
        return jsonify({"error": "Los parámetros 'fecha_inicio' y 'fecha_fin' son obligatorios"}), 400
    try:
        # Filtrar los historiales clínicos por rango de fechas
        historiales = HistorialClinico.get_by_fechas(fecha_inicio, fecha_fin)
        if not historiales:
            return jsonify({"message": "No se encontraron historiales clínicos en el rango de fechas especificado"}), 404
        # Renderizar la lista de historiales clínicos
        return jsonify(render_historial_clinico_list(historiales)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los historiales clínicos: {str(e)}"}), 400

# Eliminar un historial clínico
@historial_bp.route('/historial/<int:id_historial>', methods=['DELETE'])
@roles_required('admin', 'asistant')
def delete_historial(id_historial):
    try:
        # Validar que el historial exista
        historial = HistorialClinico.query.get(id_historial)
        if not historial:
            return jsonify({"error": "Historial clínico no encontrado"}), 404
        # Eliminar el historial clínico usando el método del modelo
        historial.delete()

        return jsonify({"message": "Historial clínico eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el historial clínico: {str(e)}"}), 400

#5