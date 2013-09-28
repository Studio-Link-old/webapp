from flask import Blueprint, render_template, url_for, redirect, flash
import alsaaudio
from app import tasks
from app.models.settings import Settings
import redis

mod = Blueprint('mixers', __name__, url_prefix='/mixers')


@mod.route('/')
def index(card=""):
    settings = Settings.query.get(1)
    if settings:
        card = settings.device
    volumes = {}
    devices = alsaaudio.cards()
    try:
        idx = devices.index(card)
    except ValueError:
        return render_template('mixers/device_error.html')
    try:
        mixers = alsaaudio.mixers(idx)
    except:
        devices = {"No ALSA Device detected"}
        return render_template('mixer.html', devices=devices, volumes=volumes)

    for i in range(len(mixers)):
        mixer = alsaaudio.Mixer(mixers[i], cardindex=idx)
        try:
            mutes = mixer.getmute()
        except alsaaudio.ALSAAudioError:
            pass
        volumes[mixers[i]] = {'mixer': i,
                              'levels': mixer.getvolume(),
                              'mutes': mutes}
    return render_template('mixers/index.html',
                           devices=devices, volumes=volumes, card=card)


@mod.route('/volume/<card>/<mixeridx>/<channel>/<value>')
def set_volume(card="", mixeridx=0, channel=0, value=50):
    #channel = alsaaudio.MIXER_CHANNEL_ALL
    devices = alsaaudio.cards()
    try:
        idx = devices.index(card)
    except ValueError:
        idx = 0
    mixers = alsaaudio.mixers(idx)
    mixer = alsaaudio.Mixer(mixers[int(mixeridx)], cardindex=idx)
    mixer.setvolume(int(value), int(channel))
    return ""


@mod.route('/muteplay/<card>/<mixeridx>/<channel>/<value>')
def mute_playback(card="", mixeridx=0, channel=0, value=0):
    devices = alsaaudio.cards()
    try:
        idx = devices.index(card)
    except ValueError:
        idx = 0
    mixers = alsaaudio.mixers(idx)
    mixer = alsaaudio.Mixer(mixers[int(mixeridx)], cardindex=idx)
    mixer.setmute(int(value), int(channel))
    return ""


@mod.route('/play/')
def play():
    flash("You should hear something...")
    store = redis.Redis('127.0.0.1')
    if store.get('lock_play_audio') != 'true':
        tasks.play_audio.delay()
    return redirect(url_for('mixers.index'))
