from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verificar que el token JWT sea válido
                verify_jwt_in_request()
                # Obtener claims del token JWT
                claims = get_jwt()
                rol = claims.get("rol")
                id_usuario = claims.get("sub")
                id_especializacion = claims.get("id_especializacion")

                # Validar que el rol está permitido
                if rol not in required_roles:
                    return jsonify({"error": "Acceso no autorizado para este rol"}), 403

                # Construir un objeto simplificado para current_user
                current_user = {
                    "id_usuario": id_usuario,
                    "rol": rol,
                    "id_especializacion": id_especializacion
                }
                # Pasar el usuario al controlador como argumento
                kwargs['current_user'] = current_user
                return fn(*args, **kwargs)
            except Exception as e:
                # Manejar errores de autenticación o JWT
                return jsonify({"error": f"Error de autenticación: {str(e)}"}), 401
        return wrapper
    return decorator
