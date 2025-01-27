from database import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)

    # Relaciones
    pedidos = db.relationship('Pedido', backref='proveedor', lazy=True)

    def __init__(self, nombre, direccion, correo_electronico):
        self.nombre = nombre
        self.direccion = direccion
        self.correo_electronico = correo_electronico

    # Métodos CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Proveedor.query.all()

    @staticmethod
    def get_by_id(id_proveedor):
        return Proveedor.query.get(id_proveedor)

    def update(self, nombre=None, direccion=None, correo_electronico=None):
        if nombre is not None:
            self.nombre = nombre
        if direccion is not None:
            self.direccion = direccion
        if correo_electronico is not None:
            self.correo_electronico = correo_electronico

        db.session.commit()

    def delete(self):
        # Verificar si hay pedidos relacionados y manejar dependencias
        if self.pedidos:
            for pedido in self.pedidos:
                pedido.id_proveedor = None  # Establecer referencia nula en los pedidos relacionados
        db.session.delete(self)
        db.session.commit()