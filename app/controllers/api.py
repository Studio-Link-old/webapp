from flask import Blueprint, request, jsonify

from app import db
from app.models.peers import Peer
from app import tasks
from sqlalchemy.exc import IntegrityError

mod = Blueprint('api', __name__, url_prefix='/api1')


@mod.route('/peers', methods=('GET', 'POST'))
def peer_invite():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': False})
    peer = Peer(request.remote_addr, request.remote_addr, 4)
    db.session.add(peer)
    db.session.commit()
    return jsonify({'result': True})


@mod.route('/peer_status')
def peer_status():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': False})
    peer = Peer.query.filter_by(host=request.remote_addr).first()
    if not peer or peer.status == 4:
        return jsonify({'result': 'denied'})
    peer.status = 1
    db.session.add(peer)
    db.session.commit()
    return jsonify({'result': request.remote_addr})
