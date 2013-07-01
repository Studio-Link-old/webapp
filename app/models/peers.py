from app import db

class Peer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    host = db.Column(db.String(100), unique=True)

    def __init__(self, name, host):
        self.name = name
        self.host = host

    def __repr__(self):
        return '<Contact %r>' % self.name
