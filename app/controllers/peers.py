from flask import Blueprint, render_template, redirect, request, url_for, flash

from app import db
from app.models.peers import Peer
from app.forms.peers import AddForm, EditForm, CallForm
from app import tasks
from sqlalchemy.exc import IntegrityError
import redis
import urllib3

http = urllib3.PoolManager(timeout=1)
mod = Blueprint('peers', __name__, url_prefix='/peers')


@mod.route('/')
def index():
    peers = Peer.query.all()
    return render_template("peers/index.html", peers=peers)


@mod.route('/add/', methods=('GET', 'POST'))
def add():
    ipv4 = "Empty"
    ipv6 = "Empty"
    try:
        #@TODO: Deploy ipv4.studio-connect.de and ipv6.studio-connect.de
        ipv4 = http.request('GET', 'http://37.187.56.6/').data
        ipv6 = http.request('GET', 'http://[2001:41d0:b:406::1]/').data
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
            flash(u'IPv6 address already exist', 'error')
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


@mod.route('/call/', methods=('GET', 'POST'))
def call():
    form = CallForm()
    if form.validate_on_submit():
        store = redis.Redis('127.0.0.1')
        store.set('lock_audio_stream', 'true')
        tasks.rtp_tx.delay()
        tasks.rtp_rx.delay()
        flash(u'RingRingRing ;-)', 'warning')
        return redirect(url_for('peers.index'))
    return render_template("peers/call.html", form=form)


@mod.route('/accept/<id>')
def accept(id):
    peer = Peer.query.get(id)
    peer.status = 0
    db.session.add(peer)
    db.session.commit()
    return redirect(url_for('peers.index'))
