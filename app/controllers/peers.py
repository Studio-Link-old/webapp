from flask import Blueprint, render_template, redirect, request, url_for, flash

from app import db
from app.models.peers import Peer
from app.models.peers import STATUS
from app.forms.peers import AddForm, EditForm, CallForm
from app import tasks
from sqlalchemy.exc import IntegrityError
import redis
import urllib3

http = urllib3.PoolManager(timeout=1)
store = redis.Redis('127.0.0.1')
mod = Blueprint('peers', __name__, url_prefix='/peers')


@mod.route('/')
def index():
    if store.get('lock_audio_stream') != 'true':
        peers = Peer.query.all()
        return render_template("peers/index.html", peers=peers)
    else:
        return render_template("peers/oncall.html")


@mod.route('/add/', methods=('GET', 'POST'))
def add():
    ipv4 = "Empty"
    ipv6 = "Empty"
    try:
        ipv4 = http.request('GET', 'http://ipv4.studio-connect.de/').data
        ipv6 = http.request('GET', 'http://ipv6.studio-connect.de/').data
    except:
        pass

    form = AddForm(request.form)
    if form.validate_on_submit():
        peer = Peer(name=form.name.data, host=form.host.data)
        db.session.add(peer)
        try:
            db.session.commit()
            tasks.api_peer_invite.delay(form.host.data)
            return redirect(url_for('peers.index'))
        except IntegrityError:
            flash(u'IPv6 address already exist', 'danger')
    return render_template("peers/form.html", form=form, ipv4=ipv4, ipv6=ipv6)


@mod.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    peer = Peer.query.get(id)
    form = EditForm(obj=peer)
    if form.validate_on_submit():
        form.populate_obj(peer)
        db.session.add(peer)
        db.session.commit()
        return redirect(url_for('peers.index'))
    return render_template("peers/form.html",
                           form=form, action='/peers/edit/'+id)


@mod.route('/delete/<id>')
def delete(id):
    db.session.delete(Peer.query.get(id))
    db.session.commit()
    return redirect(url_for('peers.index'))


@mod.route('/call/<id>', methods=('GET', 'POST'))
def call(id):
    peer = Peer.query.get(id)
    form = CallForm()
    if form.validate_on_submit():
        store.set('lock_audio_stream', 'true')
        store.set('audio_stream_host', peer.host)
        tasks.rtp_tx.delay(peer.host)
        tasks.rtp_rx.delay(peer.host)
        http.request('GET', 'http://['+peer.host+']/api1/incoming_call/')
        flash(u'RingRingRing ;-)', 'warning')
        return redirect(url_for('peers.index'))
    return render_template("peers/call.html", form=form, action='/peers/call/'+id)

@mod.route('/cancel_call/')
def cancel_call():
    store.set('lock_audio_stream', 'false')
    host = store.get('audio_stream_host')
    http.request('GET', 'http://['+host+']/cancel_call/')
    flash(u'Call canceld', 'warning')
    return redirect(url_for('peers.index'))

@mod.route('/accept/<id>')
def accept(id):
    peer = Peer.query.get(id)
    peer.status = STATUS['PENDING']
    db.session.add(peer)
    db.session.commit()
    tasks.api_peer_status.delay(peer.host)
    return redirect(url_for('peers.index'))
