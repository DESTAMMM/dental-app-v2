from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.usuario_model import Usuario
from models.roles_model import Rol

def roles_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verificar que el token JWT sea válido
                verify_jwt_in_request()
                # Obtener la identidad del usuario desde el token
                current_user_id = get_jwt_identity()
                # Consultar al usuario desde la base de datos
                usuario = Usuario.query.get(current_user_id)
                if not usuario:
                    return jsonify({"error": "Usuario no encontrado"}), 404
                # Verificar que el usuario tenga uno de los roles requeridos
                if usuario.rol.nombre_rol not in required_roles:
                    return jsonify({"error": "Acceso no autorizado para este rol"}), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": f"Error de autenticación: {str(e)}"}), 401
        return wrapper
    return decorator