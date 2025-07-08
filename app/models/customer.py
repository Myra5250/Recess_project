from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable = False)

def __init__(self, name, email, phone_number, password):
        super(Customer, self).__init__()
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        

def get_customer(self):
        return f'{self.name} {self.email}'
