from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask.cli import with_appcontext

# Importar Blueprints desde los controladores
from controllers.historial_clinico_controller import historial_bp
from controllers.inventario_controller import inventario_bp
from controllers.usuarios_controller import usuarios_bp
from controllers.citas_controller import citas_bp
from controllers.facturas_controller import facturas_bp
from database import db
import click

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración básica
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica_dental.db'  # Base de datos SQLite
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Clave secreta para JWT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(historial_bp, url_prefix='/api')
app.register_blueprint(inventario_bp, url_prefix='/api')
app.register_blueprint(usuarios_bp, url_prefix='/api')
app.register_blueprint(citas_bp, url_prefix='/api')
app.register_blueprint(facturas_bp, url_prefix='/api')

# Ruta raíz de prueba
@app.route('/')
def index():
    return "Bienvenido al sistema de gestión de la clínica dental"

# Comando para inicializar base de datos y datos básicos
@click.command(name='create_tables_and_seed')
@with_appcontext
def create_tables_and_seed():
    db.create_all()

    # Crear roles básicos
    from models.roles_model import Rol
    if not Rol.query.first():
        roles = [
            Rol(nombre_rol='admin'),
            Rol(nombre_rol='asistant'),
            Rol(nombre_rol='paciente')
        ]
        db.session.bulk_save_objects(roles)
        db.session.commit()

    # Crear usuario administrador
    from models.usuario_model import Usuario
    from models.doctor_model import Doctor
    from werkzeug.security import generate_password_hash
    if not Usuario.query.filter_by(nombre_usuario='admin').first():
        admin = Usuario(
            nombre_usuario='admin',
            contrasena=generate_password_hash('admin123'),
            id_rol=1,  # Suponiendo que el rol admin tiene ID 1
            nombre='Admin',
            apellido='User',
            correo_electronico='admin@clinica.com',
            telefono='123456789'
        )
        db.session.add(admin)
        db.session.commit()

        # Añadir al administrador como doctor
        doctor_admin = Doctor(
            id_usuario=admin.id_usuario,
            especialidad='General'
        )
        db.session.add(doctor_admin)
        db.session.commit()

# Agregar el comando a la app
app.cli.add_command(create_tables_and_seed)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
