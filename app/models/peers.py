from app import db

PENDING = 0
ONLINE = 1
OFFLINE = 2
BUSY = 3
INVITE = 4

STATUS = {
    PENDING: 'Pending',
    ONLINE: 'Online',
    OFFLINE: 'Offline',
    BUSY: 'Busy',
    INVITE: 'Invite'
}


class Peer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    host = db.Column(db.String(100), unique=True)
    status = db.Column(db.SmallInteger, default=PENDING)

    def __init__(self, name, host, status=PENDING):
        self.name = name
        self.host = host
        self.status = status

    def __repr__(self):
        return '<Contact %r>' % self.name
