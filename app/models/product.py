from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='products')

def __init__(self, name, description, price, stock):
        super(Product, self).__init__()
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

def product(self):
        return f'{self.name} {self.description}'