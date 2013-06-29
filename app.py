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

@app.route('/broadcast')
def broadcast():
    return render_template('broadcast.html')


@app.route('/mixer')
@app.route('/mixer/<card>')
def mixer(card=""):
    volumes = {}
    devices = alsaaudio.cards()
    try:
        idx=devices.index(card)
    except ValueError:
        idx=0
        card=devices[0]
    try:
        mixers = alsaaudio.mixers(idx)
    except:
        devices = {"No ALSA Device detected"}
        return render_template('mixer.html', devices=devices, volumes=volumes)

    for i in range(len(mixers)):
        mixer = alsaaudio.Mixer(mixers[i], cardindex=idx)
        volumes[mixers[i]] = {'mixer': i, 'levels': mixer.getvolume(), 'mutes': mixer.getmute()}
    return render_template('mixer.html', devices=devices, volumes=volumes, card=card)

@app.route('/mixer/volume/<card>/<mixeridx>/<channel>/<value>')
def set_volume(card="",mixeridx=0,channel=0,value=50):
    #channel = alsaaudio.MIXER_CHANNEL_ALL
    devices = alsaaudio.cards()
    try:
        idx=devices.index(card)
    except ValueError:
        idx=0
    mixers = alsaaudio.mixers(idx)
    mixer = alsaaudio.Mixer(mixers[int(mixeridx)], cardindex=idx)
    mixer.setvolume(int(value), int(channel))
    return ""

@app.route('/mixer/muteplay/<card>/<mixeridx>/<channel>/<value>')
def mute_playback(card="",mixeridx=0,channel=0,value=0):
    devices = alsaaudio.cards()
    try:
        idx=devices.index(card)
    except ValueError:
        idx=0
    mixers = alsaaudio.mixers(idx)
    mixer = alsaaudio.Mixer(mixers[int(mixeridx)], cardindex=idx)
    mixer.setmute(int(value), int(channel))
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0')
