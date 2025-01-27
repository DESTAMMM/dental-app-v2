from database import db

class Inventario(db.Model):
    __tablename__ = "inventario"
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=True)

    pedidos = db.relationship("Pedido", backref="producto", cascade="all, delete-orphan", passive_deletes=True)


    def __init__(self, nombre_producto, categoria, cantidad, fecha_ingreso, fecha_vencimiento=None):
        self.nombre_producto = nombre_producto
        self.categoria = categoria
        self.cantidad = cantidad
        self.fecha_ingreso = fecha_ingreso
        self.fecha_vencimiento = fecha_vencimiento

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Inventario.query.all()

    @staticmethod
    def get_by_id(id_producto):
        return Inventario.query.get(id_producto)

    def update(self, nombre_producto=None, categoria=None, cantidad=None, fecha_ingreso=None, fecha_vencimiento=None):
        if nombre_producto is not None:
            self.nombre_producto = nombre_producto
        if categoria is not None:
            self.categoria = categoria
        if cantidad is not None:
            self.cantidad = cantidad
        if fecha_ingreso is not None:
            self.fecha_ingreso = fecha_ingreso
        if fecha_vencimiento is not None:
            self.fecha_vencimiento = fecha_vencimiento
        db.session.commit()

    def delete(self):
        # Verificar si hay pedidos relacionados y manejar dependencias
        if self.pedidos:
            for pedido in self.pedidos:
                pedido.id_producto = None  # Establecer referencia nula en los pedidos relacionados
        db.session.delete(self)
        db.session.commit()
