from database import db

class Paciente(db.Model):
    __tablename__ = "pacientes"

    id_paciente = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)

    def __init__(self, id_usuario, fecha_nacimiento, direccion):
        self.id_usuario = id_usuario
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Paciente.query.all()

    @staticmethod
    def get_by_id(id_paciente):
        return Paciente.query.get(id_paciente)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()