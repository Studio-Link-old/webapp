from flask import Blueprint, request, jsonify

from app import db
from app.models.peers import Peer
from app import tasks
from sqlalchemy.exc import IntegrityError

mod = Blueprint('api', __name__, url_prefix='/api1')

@mod.route('/peers', methods=('GET', 'POST'))
def peer_invite():
    peer = Peer(request.remote_addr, request.remote_addr, 4)
    db.session.add(peer)
    db.session.commit()
    return jsonify({'result': True })

@mod.route('/peer_status')
def peer_status():
    peer = Peer.query.filter_by(host=request.remote_addr).first()
    if not peer:
        return jsonify({'result': 'denied'})
    peer.status = 1
    db.session.add(peer)
    db.session.commit()
    return jsonify({'result': request.remote_addr})
