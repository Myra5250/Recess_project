from app import db

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable = False)
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), default='customer')

    def __init__(self, name, email, phone_number, password, is_admin=False, role='customer'):
        
        super(Customer, self).__init__()
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.is_admin = is_admin
        self.role = role

    def get_customer(self):
       return f'{self.name}'

    def __repr__(self):
        return f'<Customer {self.name}>'


