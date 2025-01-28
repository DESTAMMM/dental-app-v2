from database import db

class Doctor(db.Model):
    __tablename__ = "doctores"

    id_doctor = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    especialidad = db.Column(db.String(255), nullable=False)

    # Relación con Usuario
    usuario = db.relationship("Usuario", back_populates="doctor", cascade="all, delete-orphan",  single_parent=True)

    def __init__(self, id_usuario, especialidad):
        self.id_usuario = id_usuario
        self.especialidad = especialidad

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Doctor.query.all()

    @staticmethod
    def get_by_id(id_doctor):
        return Doctor.query.get(id_doctor)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()