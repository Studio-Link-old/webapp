from flask import Blueprint, request, jsonify

from app import db
from app.models.peers import Peer
from app import tasks
from sqlalchemy.exc import IntegrityError
import socket
import redis

mod = Blueprint('api', __name__, url_prefix='/api1')
store = redis.Redis('127.0.0.1')


@mod.route('/peers/', methods=('GET', 'POST'))
def peer_invite():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': 'denied'})
    peer = Peer(request.remote_addr, request.remote_addr, 4)
    db.session.add(peer)
    db.session.commit()
    return jsonify({'result': True})


@mod.route('/peer_status/')
def peer_status():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': 'denied'})
    peer = Peer.query.filter_by(host=request.remote_addr).first()
    if not peer or peer.status == 4:
        return jsonify({'result': 'denied'})
    peer.status = 1
    db.session.add(peer)
    db.session.commit()
    return jsonify({'result': request.remote_addr})


@mod.route('/incoming_call/')
def incoming_call():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': 'denied'})
    peer = Peer.query.filter_by(host=request.remote_addr).first()
    if not peer or peer.status == 4:
        return jsonify({'result': 'denied'})
    store.set('lock_audio_stream', 'true')
    tasks.rtp_tx.delay(request.remote_addr)
    tasks.rtp_rx.delay(request.remote_addr)
    return jsonify({'result': request.remote_addr})


@mod.route('/cancel_call/')
def cancel_call():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': 'denied'})
    peer = Peer.query.filter_by(host=request.remote_addr).first()
    if not peer or peer.status == 4:
        return jsonify({'result': 'denied'})
    store.set('lock_audio_stream', 'false')
    return jsonify({'result': request.remote_addr})
