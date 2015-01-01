# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          __    _       __                      |
# |  / ___// /___  ______/ (_)___     / /   (_)___  / /__                    |
# |  \__ \/ __/ / / / __  / / __ \   / /   / / __ \/ //_/                    |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ / / / / ,<                       |
# |/____/\__/\__,_/\__,_/_/\____/  /_____/_/_/ /_/_/|_|                      |
# |Copyright Sebastian Reimers 2013 - 2015 studio-link.de                    |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask import Blueprint, render_template, url_for, redirect, flash
import alsaaudio
from app.models.settings import Settings
from app.libs import baresip

mod = Blueprint('mixers', __name__, url_prefix='/mixers')


@mod.route('/')
def index(card=""):
    settings = Settings.query.get(1)
    if settings:
        card = settings.device
    playbacks = {}
    captures = {}
    devices = alsaaudio.cards()
    try:
        idx = devices.index(card)
    except ValueError:
        return render_template('mixers/device_error.html')
    try:
        mixers = alsaaudio.mixers(idx)
    except:
        devices = {"No ALSA Device detected"}
        return render_template('mixers/index.html', devices=devices,
                               playbacks=playbacks, captures=captures)

    for i in range(len(mixers)):
        mixer = alsaaudio.Mixer(mixers[i], cardindex=idx)

        try:
            mutes = mixer.getmute()
        except alsaaudio.ALSAAudioError:
            mutes = {}

        try:
            getrecs = mixer.getrec()
        except alsaaudio.ALSAAudioError:
            getrecs = {}

        if mixer.getvolume('playback'):
            playbacks[mixers[i]] = {'mixer': i,
                                    'levels': mixer.getvolume('playback'),
                                    'mutes': mutes}
        if mixer.getvolume('capture'):
            captures[mixers[i]] = {'mixer': i,
                                   'levels': mixer.getvolume('capture'),
                                   'mutes': getrecs}

    return render_template('mixers/index.html',
                           devices=devices,
                           playbacks=playbacks,
                           captures=captures,
                           card=card)


@mod.route('/volume/<card>/<mixeridx>/<channel>/<value>/<direction>')
def set_volume(card="", mixeridx=0, channel=0, value=50, direction='playback'):
    # channel = alsaaudio.MIXER_CHANNEL_ALL
    devices = alsaaudio.cards()
    try:
        idx = devices.index(card)
    except ValueError:
        idx = 0
    mixers = alsaaudio.mixers(idx)
    mixer = alsaaudio.Mixer(mixers[int(mixeridx)], cardindex=idx)
    mixer.setvolume(int(value), int(channel), direction)
    return ""


@mod.route('/mute/<direction>/<card>/<mixeridx>/<channel>/<value>')
def mute(direction="playback", card="", mixeridx=0, channel=0, value=0):
    devices = alsaaudio.cards()
    try:
        idx = devices.index(card)
    except ValueError:
        idx = 0
    mixers = alsaaudio.mixers(idx)
    mixer = alsaaudio.Mixer(mixers[int(mixeridx)], cardindex=idx)
    if direction == "playback":
        mixer.setmute(int(value), int(channel))
    else:
        mixer.setrec(int(value), int(channel))
    return ""


@mod.route('/play/<status>')
def play(status="false"):
    if status == 'true':
        r = baresip.set('start_audio_loop')
        flash('You should hear something... '+r, 'info')
    else:
        r = baresip.set('stop_audio_loop')
        flash('The audio loop stops... '+r, 'info')
    return redirect(url_for('mixers.index'))
