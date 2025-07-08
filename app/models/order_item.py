from app import db

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')

def __init__(self, quantity, price):
        super(OrderItem, self).__init__()
        self.quantity = quantity
        self.price = price

def get_order_item(self):
        return f'{self.quantity} {self.price}'