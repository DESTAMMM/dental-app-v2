from database import db

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('facturas.id_factura'), nullable=False)
    descripcion_tratamiento = db.Column(db.String(255), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    id_doctor = db.Column(db.Integer, db.ForeignKey('doctores.id_doctor'), nullable=False)
    fecha_tratamiento = db.Column(db.Date, nullable=False)

    def __init__(self, id_factura, descripcion_tratamiento, costo, id_doctor, fecha_tratamiento):
        self.id_factura = id_factura
        self.descripcion_tratamiento = descripcion_tratamiento
        self.costo = costo
        self.id_doctor = id_doctor
        self.fecha_tratamiento = fecha_tratamiento

    # Métodos CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return DetalleFactura.query.all()

    @staticmethod
    def get_by_id(id_detalle):
        return DetalleFactura.query.get(id_detalle)

    def update(self, descripcion_tratamiento=None, costo=None, fecha_tratamiento=None):
        if descripcion_tratamiento is not None:
            self.descripcion_tratamiento = descripcion_tratamiento
        if costo is not None:
            self.costo = costo
        if fecha_tratamiento is not None:
            self.fecha_tratamiento = fecha_tratamiento

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()