from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)


def __init__(self, username):
        super(Admin, self).__init__()
        self.username = username

def __repr__(self):
    return f"{self.username}"