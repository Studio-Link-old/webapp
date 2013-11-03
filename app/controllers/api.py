# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          ______                            __  |
# |  / ___// /___  ______/ (_)___     / ____/___  ____  ____  ___  _____/ /_ |
# |  \__ \/ __/ / / / __  / / __ \   / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/ |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ /_/ / / / / / / /  __/ /__/ /_   |
# |/____/\__/\__,_/\__,_/_/\____/   \____/\____/_/ /_/_/ /_/\___/\___/\__/   |
# |Copyright Sebastian Reimers 2013 studio-connect.de                        |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask import Blueprint, request, jsonify

from app import db
from app.models.peers import Peer
from app.models.peers import STATUS
from app import tasks
from sqlalchemy.exc import IntegrityError
import socket
import redis
from subprocess import call

mod = Blueprint('api', __name__, url_prefix='/api1')
store = redis.Redis('127.0.0.1')


@mod.route('/peers/', methods=('GET', 'POST'))
def peer_invite():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': 'denied'})
    peer = Peer(request.remote_addr, request.remote_addr, STATUS['INVITE'])
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
    if not peer or peer.status == STATUS['INVITE']:
        return jsonify({'result': 'denied'})
    peer.status = STATUS['ONLINE']
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
    if not peer or peer.status == STATUS['INVITE']:
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
    if not peer or peer.status == STATUS['INVITE']:
        return jsonify({'result': 'denied'})
    store.set('lock_audio_stream', 'false')
    call("sudo systemctl restart studio-celery", shell=True)
    call("sudo systemctl restart studio-celery2", shell=True)
    return jsonify({'result': request.remote_addr})


@mod.route('/audio_caps/')
def audio_caps():
    try:
        socket.inet_pton(socket.AF_INET6, request.remote_addr)
    except socket.error:
        return jsonify({'result': 'denied'})
    peer = Peer.query.filter_by(host=request.remote_addr).first()
    if not peer or peer.status == STATUS['INVITE']:
        return jsonify({'result': 'denied'})
    return jsonify({'result': store.get('audio_caps')}) 
