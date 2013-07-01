from flask import Blueprint, render_template

from app import db
from app.models.peers import Peer

mod = Blueprint('peers', __name__, url_prefix='/peers')

@mod.route('/')
def index():
    peers = Peer.query.all()
    return render_template("peers/index.html", peers=peers)

@mod.route('/add/')
def add():
    peer = Peer('test3', 'test1.hugo-will-es-wissen.example.com')
    db.session.add(peer)
    db.session.commit()
    return render_template("peers/add.html")
