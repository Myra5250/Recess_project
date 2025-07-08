from app import db

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', backref='carts')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

def __init__(self, customer, created_at):
        super(Cart, self).__init__()
        self.customer = customer
        self.created_at = created_at

def cart(self):
        return f'{self.customer} {self.created_at}'