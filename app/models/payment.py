from app import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    method = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

def __init__(self, method, amount, timestamp):
        super(Payment, self).__init__()
        self.method = method
        self.amount = amount
        self.timestamp = timestamp
#change def
def payment(self):
        return f'{self.method} {self.amount}'