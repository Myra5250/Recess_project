from app.extensions import db

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product')

def __init__(self, quantity):
        super(CartItem, self).__init__()
        self.quantity = quantity

def cart_item(self):
        return f'{self.quantity}'