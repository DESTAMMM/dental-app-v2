from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from database import db
from models import Usuario, Rol  # Asegúrate de importar tus modelos

def roles_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                
                # Consultar el usuario y su rol desde la base de datos
                usuario = Usuario.query.get(current_user_id)
                if not usuario or usuario.rol.nombre_rol not in required_roles:
                    return jsonify({"error": "Acceso no autorizado para este rol"}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": str(e)}), 401
        return wrapper
    return decorator