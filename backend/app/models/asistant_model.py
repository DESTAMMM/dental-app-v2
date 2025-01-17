from database import db
class Asistente(db.Model):
    __tablename__ = "asistentes"

    id_asistente = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_contratacion = db.Column(db.Date, nullable=False)
    turno = db.Column(db.String(50), nullable=False)
    area_especialidad = db.Column(db.String(255), nullable=False)

    def __init__(self, id_usuario, fecha_contratacion, turno, area_especialidad):
        self.id_usuario = id_usuario
        self.fecha_contratacion = fecha_contratacion
        self.turno = turno
        self.area_especialidad = area_especialidad

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Asistente.query.all()

    @staticmethod
    def get_by_id(id_asistente):
        return Asistente.query.get(id_asistente)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()