from app import db


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(120), unique=True)

    def __init__(self, device):
        self.device = device

    def __repr__(self):
        return '<Device %r>' % self.device
