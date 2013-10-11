from app import db

STATUS = {
    'PENDING': 0,
    'ONLINE': 1,
    'OFFLINE': 2,
    'BUSY': 3,
    'INVITE': 4
}


class Peer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    host = db.Column(db.String(100), unique=True)
    status = db.Column(db.SmallInteger, default=STATUS['PENDING'])

    def __init__(self, name, host, status=STATUS['PENDING']):
        self.name = name
        self.host = host
        self.status = status
