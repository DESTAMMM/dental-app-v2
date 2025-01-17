from flask import Blueprint, request, jsonify
from models.citas import Cita
from models.doctores import Doctor
from models.pacientes import Paciente
from utils.auth_decorators import roles_required
from database import db
from sqlalchemy.orm import joinedload
from datetime import datetime

citas_bp = Blueprint('citas', __name__)

@citas_bp.route('/doctores_pacientes_citas', methods=['GET'])
@roles_required('admin', 'asistente')
def get_doctores_pacientes_citas():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    # Validar las fechas
    if not fecha_inicio or not fecha_fin:
        return jsonify({"error": "Fechas no proporcionadas"}), 400
    # Convertir las fechas a objetos datetime
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    # Consultar citas en el rango de fechas
    citas = Cita.query.options(
        joinedload(Cita.doctor).joinedload(Doctor.usuario),
        joinedload(Cita.paciente).joinedload(Paciente.usuario)
    ).filter(
        Cita.fecha_cita >= fecha_inicio_dt,
        Cita.fecha_cita <= fecha_fin_dt
    ).all()
    # Crear una lista de doctores con sus pacientes y citas en el rango de fechas
    doctores_dict = {}
    for cita in citas:
        doctor_id = cita.id_doctor
        if doctor_id not in doctores_dict:
            doctores_dict[doctor_id] = {
                "nombre_doctor": cita.doctor.usuario.nombre,
                "pacientes": []
            }
        doctores_dict[doctor_id]["pacientes"].append({
            "nombre_paciente": cita.paciente.usuario.nombre,
            "fecha_cita": cita.fecha_cita.strftime('%Y-%m-%d'),
            "hora_cita": cita.hora_cita,
            "motivo_cita": cita.motivo_cita,
            "estado": cita.estado
        })
    # Convertir el diccionario a una lista para la respuesta JSON
    doctores_list = [
        {
            "nombre_doctor": doctor_data["nombre_doctor"],
            "pacientes": doctor_data["pacientes"]
        } for doctor_data in doctores_dict.values()
    ]
    return jsonify(doctores_list), 200
