from app import db

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rssfeed = db.Column(db.String(120), unique = True)

    def __init__(self, rssfeed):
        self.rssfeed = rssfeed

    def __repr__(self):
        return '<NZBMatrix feed url %r>' % self.rssfeed
