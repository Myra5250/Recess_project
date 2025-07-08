from app import db

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

def __init__(self, customer_name, content, created_at):
        super(Testimonial, self).__init__()
        self.customer_name = customer_name
        self.content = content
        self.created_at = created_at
##change def
def get_full_name(self):
        return f'{self.customer_name} {self.content}'