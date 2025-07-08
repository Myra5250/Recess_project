from app import db

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

def __init__(self, name, email, message, timestamp):
        super(Inquiry, self).__init__()
        self.name = name
        self.email = email
        self.message = message
        self.timestamp = timestamp

def inquiry(self):
        return f'{self.name} {self.email}'