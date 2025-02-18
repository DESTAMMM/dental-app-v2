from database import db

class HistorialClinico(db.Model):
    __tablename__ = "historial_clinico"
    id_historial = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey("pacientes.id_paciente"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    diagnostico = db.Column(db.String(255), nullable=False)
    tratamiento = db.Column(db.String(255), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    
    paciente = db.relationship("Paciente", backref=db.backref("historiales", cascade="all, delete-orphan"))
    
    def __init__(self, id_paciente, fecha, diagnostico, tratamiento, observaciones=None):
        self.id_paciente = id_paciente
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return HistorialClinico.query.all()

    @staticmethod
    def get_by_id(id_historial):
        return HistorialClinico.query.get(id_historial)
    
    @staticmethod
    def get_by_fechas(fecha_inicio, fecha_fin):
        return HistorialClinico.query.filter(
            HistorialClinico.fecha >= fecha_inicio,
            HistorialClinico.fecha <= fecha_fin
        ).all()
    
    @staticmethod
    def get_by_pacientes(ids_pacientes):       
        return HistorialClinico.query.filter(HistorialClinico.id_paciente.in_(ids_pacientes)).all()

    
    def update(self, fecha=None, diagnostico=None, tratamiento=None, observaciones=None):
        if fecha is not None:
            self.fecha = fecha
        if diagnostico is not None:
            self.diagnostico = diagnostico
        if tratamiento is not None:
            self.tratamiento = tratamiento
        if observaciones is not None:
            self.observaciones = observaciones
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
