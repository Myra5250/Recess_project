from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    customer = db.relationship('Customer')

def __init__(self, total_amount, status, created_at):
        super(Order, self).__init__()
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at

def order(self):
        return f'{self.total_amount} {self.status}'