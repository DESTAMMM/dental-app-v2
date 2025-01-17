from database import db
from werkzeug.security import generate_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id_rol"), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)

    def __init__(self, nombre_usuario, contrasena, id_rol, nombre, apellido, correo_electronico, telefono):
        self.nombre_usuario = nombre_usuario
        self.set_password(contrasena)
        self.id_rol = id_rol
        self.nombre = nombre
        self.apellido = apellido
        self.correo_electronico = correo_electronico
        self.telefono = telefono

    def set_password(self, contrasena):
        self.contrasena = generate_password_hash(contrasena)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def get_by_id(id_usuario):
        return Usuario.query.get(id_usuario)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
