from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def roles_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verificar que el token JWT sea válido
                verify_jwt_in_request()
                # Obtener la identidad del usuario desde el token
                current_user_id = get_jwt_identity()
                # Importar dinámicamente los modelos para evitar dependencias circulares
                from models.usuario_model import Usuario
                # Consultar al usuario desde la base de datos con su rol
                usuario = Usuario.query.filter_by(id_usuario=current_user_id).join("rol").first()
                if not usuario:
                    return jsonify({"error": "Usuario no encontrado"}), 404
                # Verificar que el rol del usuario está permitido
                if usuario.rol.nombre_rol not in required_roles:
                    return jsonify({"error": "Acceso no autorizado para este rol"}), 403

                # Pasar el usuario al controlador como argumento
                kwargs['current_user'] = usuario
                return fn(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": f"Error de autenticación: {str(e)}"}), 401
        return wrapper
    return decorator
