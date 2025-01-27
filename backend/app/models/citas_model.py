from database import db

class Cita(db.Model):
    __tablename__ = 'citas'

    id_cita = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    fecha_cita = db.Column(db.Date, nullable=False)
    hora_cita = db.Column(db.Time, nullable=False)
    motivo_cita = db.Column(db.String(255), nullable=False)
    id_doctor = db.Column(db.Integer, db.ForeignKey('doctores.id_doctor'), nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    paciente = db.relationship("Paciente", backref=db.backref("citas", cascade="all, delete-orphan"))
    doctor = db.relationship("Doctor", backref="citas")

    def __init__(self, id_paciente, id_doctor, fecha_cita, hora_cita, motivo_cita, estado):
        self.id_paciente = id_paciente
        self.id_doctor = id_doctor
        self.fecha_cita = fecha_cita
        self.hora_cita = hora_cita
        self.motivo_cita = motivo_cita
        self.estado = estado

    # Métodos CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cita.query.all()

    @staticmethod
    def get_by_id(id_cita):
        return Cita.query.get(id_cita)

    def update(self, fecha_cita=None, hora_cita=None, motivo_cita=None, estado=None):
        if fecha_cita is not None:
            self.fecha_cita = fecha_cita
        if hora_cita is not None:
            self.hora_cita = hora_cita
        if motivo_cita is not None:
            self.motivo_cita = motivo_cita
        if estado is not None:
            self.estado = estado

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()