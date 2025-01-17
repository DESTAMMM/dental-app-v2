from database import db

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey("inventario.id_producto"), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedores.id_proveedor"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_pedido = db.Column(db.Date, nullable=False)
    fecha_entrega = db.Column(db.Date, nullable=True)
    estado_pedido = db.Column(db.String(50), nullable=False)

    producto = db.relationship("Inventario", backref="pedidos")
    proveedor = db.relationship("Proveedor", backref="pedidos")

    def __init__(self, id_producto, id_proveedor, cantidad, fecha_pedido, estado_pedido, fecha_entrega=None):
        self.id_producto = id_producto
        self.id_proveedor = id_proveedor
        self.cantidad = cantidad
        self.fecha_pedido = fecha_pedido
        self.estado_pedido = estado_pedido
        self.fecha_entrega = fecha_entrega

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Pedido.query.all()

    @staticmethod
    def get_by_id(id_pedido):
        return Pedido.query.get(id_pedido)

    def update(self, cantidad=None, fecha_pedido=None, fecha_entrega=None, estado_pedido=None):
        if cantidad is not None:
            self.cantidad = cantidad
        if fecha_pedido is not None:
            self.fecha_pedido = fecha_pedido
        if fecha_entrega is not None:
            self.fecha_entrega = fecha_entrega
        if estado_pedido is not None:
            self.estado_pedido = estado_pedido
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
