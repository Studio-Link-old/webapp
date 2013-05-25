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
def alsa(idx=0):
    mixers = alsaaudio.mixers(idx)
    mixer = alsaaudio.Mixer(mixers[0], cardindex=idx)
    volumes = mixer.getvolume()
    volumes_txt = ""
    for i in range(len(volumes)):
        volumes_txt = volumes_txt + "Channel %i volume: %i%%\n" % (i,volumes[i])

    return render_template('alsa.html', mixers=mixers, volumes=volumes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
