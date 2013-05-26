#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Podlove Raspberry
    ~~~~~~~~~~~~~~~~~

    A raspberry web application for audio broadcasting and more.

    :copyright: (c) 2013 by Sebastian Reimers.
    :license: BSD 2-Clause, see LICENSE for more details.
"""
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
import alsaaudio
from subprocess import Popen, PIPE, STDOUT
from flaskext.babel import Babel


app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = True
Babel(app)

#Loading settings
app.config.from_object('settings')

@app.route('/')
def index():
    p = Popen('uptime', stdout=PIPE, stderr=STDOUT, close_fds=True)
    uptime = p.stdout.read()
    return render_template('index.html', uptime=uptime)

@app.route('/openob')
def openob():
    return render_template('openob.html')

@app.route('/sip')
def sip():
    return render_template('sip.html')

@app.route('/alsa')
@app.route('/alsa/<card>')
def alsa(card="ALSA"):
    devices = alsaaudio.cards()
    try:
        idx=devices.index(card)
    except ValueError:
        card = "ALSA"
        idx=devices.index(card)
    mixers = alsaaudio.mixers(idx)
    volumes = {}
    for i in range(len(mixers)):
        mixer = alsaaudio.Mixer(mixers[i], cardindex=idx)
        volumes[mixers[i]] = {'levels': mixer.getvolume(), 'mutes': mixer.getmute()}

    return render_template('alsa.html', devices=devices, volumes=volumes)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
