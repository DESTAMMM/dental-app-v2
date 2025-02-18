from flask import Blueprint, request, jsonify
from models.usuario_model import Usuario
from models.paciente_model import Paciente
from models.doctor_model import Doctor
from models.asistente_model import Asistente
from models.roles_model import Rol
from utils.decorator import roles_required
from views.usuarios_view import render_user_list, render_user_detail
from views.pacientes_view import render_paciente_list, render_paciente_detail
from views.doctores_view import render_doctor_list, render_doctor_detail
from views.asistentes_view import render_asistente_list, render_asistente_detail
from sqlalchemy.orm import joinedload
from flask_jwt_extended import create_access_token, get_jwt

usuarios_bp = Blueprint('usuarios', __name__)

# Función auxiliar para manejar errores
def handle_not_found(message="Recurso no encontrado"):
    return jsonify({"error": message}), 404

# Función auxiliar para obtener un rol por nombre
def get_role_by_name(role_name):
    return Rol.query.filter_by(nombre_rol=role_name).first() 

# Función auxiliar para crear un usuario
def create_user(data, role_id):
    # Verificar si el nombre de usuario ya existe
    if Usuario.get_by_nombre_usuario(data['nombre_usuario']):
        raise ValueError("El nombre de usuario ya existe")

    nuevo_usuario = Usuario(
        nombre_usuario=data['nombre_usuario'],
        contrasena=data['contrasena'],
        id_rol=role_id,
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo_electronico=data['correo_electronico'],
        telefono=data.get('telefono')
    )
    nuevo_usuario.save()
    return nuevo_usuario

# Registro público (siempre como paciente)
@usuarios_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        role = get_role_by_name("paciente")
        if not role:
            return jsonify({"error": "El rol 'paciente' no está configurado"}), 500
        # Crear usuario utilizando la función auxiliar
        nuevo_usuario = create_user(data, role.id_rol)
        # Crear paciente relacionado
        nuevo_paciente = Paciente(
            id_usuario=nuevo_usuario.id_usuario,
            fecha_nacimiento=data['fecha_nacimiento'],
            direccion=data['direccion']
        )
        nuevo_paciente.save()
        return jsonify({"message": "Usuario registrado exitosamente como paciente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al registrar el usuario: {str(e)}"}), 400

# Crear doctor (Solo admin)
@usuarios_bp.route('/create_doctor', methods=['POST'])
@roles_required('admin')
def create_doctor():
    data = request.get_json()
    try:
        role = get_role_by_name("doctor")
        if not role:
            return jsonify({"error": "El rol 'doctor' no está configurado"}), 500
        # Crear usuario utilizando la función auxiliar
        nuevo_usuario = create_user(data, role.id_rol)
        # Crear doctor relacionado
        nuevo_doctor = Doctor(
            id_usuario=nuevo_usuario.id_usuario,
            especialidad=data['especialidad']
        )
        nuevo_doctor.save()

        return jsonify({"message": "Doctor creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el doctor: {str(e)}"}), 400

# Crear asistente (admin o asistente)
@usuarios_bp.route('/create_asistente', methods=['POST'])
@roles_required('admin', 'asistant')
def create_asistente():
    data = request.get_json()
    try:
        role = get_role_by_name("asistant")
        if not role:
            return jsonify({"error": "El rol 'asistant' no está configurado"}), 500
        # Crear usuario utilizando la función auxiliar
        nuevo_usuario = create_user(data, role.id_rol)
        # Crear asistente relacionado
        nuevo_asistente = Asistente(
            id_usuario=nuevo_usuario.id_usuario,
            fecha_contratacion=data['fecha_contratacion'],
            turno=data['turno'],
            area_especialidad=data['area_especialidad']
        )
        nuevo_asistente.save()

        return jsonify({"message": "Asistente creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el asistente: {str(e)}"}), 400

# Obtener todos los usuarios (Solo admin)
@usuarios_bp.route('/usuarios', methods=['GET'])
@roles_required('admin', 'asistant')
def get_all_users():
    usuarios = Usuario.get_all()
    return jsonify(render_user_list(usuarios)), 200

@usuarios_bp.route('/pacientes', methods=['GET'])
@roles_required('admin')
def get_all_pacientes():
    try:
        # Consulta personalizada con joinedload
        pacientes = Paciente.query.options(
            joinedload(Paciente.usuario).joinedload("rol")
        ).all()

        if not pacientes:
            return jsonify({"message": "No se encontraron pacientes"}), 404
        # Renderizar la lista de pacientes
        return jsonify(render_paciente_list(pacientes)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los pacientes: {str(e)}"}), 400

@usuarios_bp.route('/doctores', methods=['GET'])
@roles_required('admin')
def get_all_doctores():
    try:
        # Consulta personalizada con joinedload para cargar relaciones necesarias
        doctores = Doctor.query.options(
            joinedload(Doctor.usuario).joinedload("rol")
        ).all()
        if not doctores:
            return jsonify({"message": "No se encontraron doctores"}), 404
        # Renderizar la lista de doctores con los datos del usuario y rol
        return jsonify(render_doctor_list(doctores)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los doctores: {str(e)}"}), 400

@usuarios_bp.route('/asistentes', methods=['GET'])
@roles_required('admin')
def get_all_asistentes():
    try:
        # Consulta personalizada con joinedload
        asistentes = Asistente.query.options(
            joinedload(Asistente.usuario).joinedload("rol")
        ).all()
        if not asistentes:
            return jsonify({"message": "No se encontraron asistentes"}), 404
        # Renderizar la lista de asistentes
        return jsonify(render_asistente_list(asistentes)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los asistentes: {str(e)}"}), 400

@usuarios_bp.route('/mi_informacion', methods=['GET'])
@roles_required('paciente', 'doctor', 'asistant')
def get_personal_info():
    try:
        # Extraer claims del token JWT
        claims = get_jwt()
        rol = claims.get("rol")
        id_especializacion = claims.get("id_especializacion")
        # Manejo según el rol del usuario
        if rol == 'paciente':
            paciente = Paciente.get_by_id(id_especializacion)
            if not paciente:
                return jsonify({"error": "No se encontró información del paciente"}), 404
            return jsonify(render_paciente_detail(paciente)), 200
        elif rol == 'doctor':
            doctor = Doctor.get_by_id(id_especializacion)
            if not doctor:
                return jsonify({"error": "No se encontró información del doctor"}), 404
            return jsonify(render_doctor_detail(doctor)), 200
        elif rol == 'asistant':
            asistente = Asistente.get_by_id(id_especializacion)
            if not asistente:
                return jsonify({"error": "No se encontró información del asistente"}), 404
            return jsonify(render_asistente_detail(asistente)), 200
        # Rol no reconocido
        return jsonify({"error": "Rol no reconocido"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al obtener la información personal: {str(e)}"}), 500

    
@usuarios_bp.route('/search_user', methods=['GET'])
@roles_required('admin', 'asistant')
def search_user():
    data = request.args  
    text = data.get('text')
    if not text:
        return jsonify({"error": "El parámetro 'text' es obligatorio"}), 400
    try:
        # Buscar usuarios usando el texto proporcionado
        usuarios = Usuario.get_by_nombre_o_apellido(text)
        if not usuarios:
            return jsonify({"message": "No se encontraron usuarios"}), 404
        # Renderizar la lista de usuarios encontrados
        return jsonify(render_user_list(usuarios)), 200
    except Exception as e:
        return jsonify({"error": f"Error al buscar usuarios: {str(e)}"}), 400
    
@usuarios_bp.route('/update_user', methods=['PUT'])
@roles_required('admin')
def update_user():
    data = request.get_json()
    nombre_usuario_actual = data.get('nombre_usuario')  # Identificador único del usuario actual
    nuevo_nombre_usuario = data.get('nuevo_nombre_usuario')  # Nuevo nombre de usuario (opcional)
    if not nombre_usuario_actual:
        return jsonify({"error": "El parámetro 'nombre_usuario' es obligatorio"}), 400
    
    try:
        # Buscar al usuario actual
        usuario = Usuario.get_by_nombre_usuario(nombre_usuario_actual)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        # Verificar si el nuevo nombre_usuario ya está en uso
        if nuevo_nombre_usuario and nuevo_nombre_usuario != usuario.nombre_usuario:
            usuario_existente = Usuario.get_by_nombre_usuario(nuevo_nombre_usuario)
            if usuario_existente:
                return jsonify({"error": "El nuevo 'nombre_usuario' ya está en uso"}), 400
            # Actualizar nombre_usuario
            usuario.nombre_usuario = nuevo_nombre_usuario
        # Actualizar datos básicos del usuario
        usuario.update(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            correo_electronico=data.get('correo_electronico'),
            telefono=data.get('telefono')
        )
        # Detectar y actualizar la especialización
        if usuario.doctor:
            usuario.doctor.update(especialidad=data.get('especialidad'))
        elif usuario.asistente:
            usuario.asistente.update(
                fecha_contratacion=data.get('fecha_contratacion'),
                turno=data.get('turno'),
                area_especialidad=data.get('area_especialidad')
            )
        elif usuario.paciente:
            usuario.paciente.update(
                fecha_nacimiento=data.get('fecha_nacimiento'),
                direccion=data.get('direccion')
            )
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el usuario: {str(e)}"}), 400


@usuarios_bp.route('/delete_user', methods=['DELETE'])
@roles_required('admin')
def delete_user():
    data = request.get_json()
    # Obtener el identificador único del usuario (nombre_usuario)
    nombre_usuario = data.get('nombre_usuario')
    if not nombre_usuario:
        return jsonify({"error": "Falta el identificador del usuario"}), 400
    try:
        # Buscar el usuario por nombre_usuario
        usuario = Usuario.get_by_nombre_usuario(nombre_usuario)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        usuario.delete()
        return jsonify({"message": f"Usuario '{nombre_usuario}'eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el usuario: {str(e)}"}), 400


@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    contrasena=data.get('contrasena')
    # Validar datos de entrada
    if not data.get('nombre_usuario') or not data.get('contrasena'):
        return jsonify({"error": "El nombre de usuario y la contraseña son obligatorios"}), 400
    # Buscar usuario en la base de datos
    usuario = Usuario.query.filter_by(nombre_usuario=data['nombre_usuario']).first()
    if not usuario or not usuario.check_password(contrasena):
        return jsonify({"error": "Credenciales inválidas"}), 401
    # Identificar el rol y la especialización
    if usuario.paciente:
        id_especializacion = usuario.paciente.id_paciente
        rol = "paciente"
    elif usuario.doctor:
        id_especializacion = usuario.doctor.id_doctor
        rol = "doctor"
    elif usuario.asistente:
        id_especializacion = usuario.asistente.id_asistente
        rol = "asistente"
    else:
        id_especializacion = None
        rol = "sin_especializacion"
    # Crear el JWT token con claims adicionales
    additional_claims = {
        "id_especializacion": id_especializacion,
        "rol": rol
    }
    access_token = create_access_token(identity=usuario.id_usuario, additional_claims=additional_claims)
    return jsonify({"access_token": access_token}), 200
