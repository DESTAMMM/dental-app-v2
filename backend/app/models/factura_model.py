from database import db

class Factura(db.Model):
    __tablename__ = "facturas"
    id_factura = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey("pacientes.id_paciente", ondelete="SET NULL"), nullable=True)
    fecha_factura = db.Column(db.DateTime, nullable=False)
    monto_total = db.Column(db.Float, nullable=False)
    estado_pago = db.Column(db.String(50), nullable=False)

    paciente = db.relationship("Paciente",backref=db.backref("facturas", passive_deletes=True),)
    detalles = db.relationship("DetalleFactura", backref="factura", cascade="all, delete-orphan")

    def __init__(self, id_paciente, fecha_factura, monto_total, estado_pago):
        self.id_paciente = id_paciente
        self.fecha_factura = fecha_factura
        self.monto_total = monto_total
        self.estado_pago = estado_pago

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Factura.query.all()

    @staticmethod
    def get_by_id(id_factura):
        return Factura.query.get(id_factura)

    def update(self, fecha_factura=None, monto_total=None, estado_pago=None):
        if fecha_factura is not None:
            self.fecha_factura = fecha_factura
        if monto_total is not None:
            self.monto_total = monto_total
        if estado_pago is not None:
            self.estado_pago = estado_pago
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
