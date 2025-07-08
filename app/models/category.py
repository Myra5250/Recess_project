from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))

def __init__(self, name, description):
        super(Category, self).__init__()
        self.name = name
        self.description = description

def category(self):
        return f'{self.name} {self.description}'