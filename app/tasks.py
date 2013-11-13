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

from __future__ import absolute_import
from app.celery import celery
from app.libs.audio.play import Play
from app.models.settings import Settings
from app.models.peers import Peer
from app.libs.rtp.rx import RTPreceiver
from app.libs.rtp.tx import RTPtransmitter
from gi.repository import Gst
import redis
import urllib3
import alsaaudio
import subprocess
import time
import json

http = urllib3.PoolManager(timeout=3)
store = redis.Redis('127.0.0.1')


def device_init():
    settings = Settings.query.get(1)
    devices = alsaaudio.cards()
    idx = devices.index(settings.device)
    device = 'hw:' + str(idx)
    return device


@celery.task
def rtp_tx(host):
    subprocess.call("sudo systemctl stop studio-beat &", shell=True)
    device = device_init()
    settings = Settings.query.get(1)
    audio = True
    if settings.audio == 'voice':
        audio = False
    opus_options = {'audio': audio,
                    'bandwidth': -1000,
                    'frame-size': int(settings.framesize),
                    'complexity': int(settings.complexity),
                    'constrained-vbr': True,
                    'inband-fec': True,
                    'packet-loss-percentage': 1,
                    'dtx': False}
    transmitter = RTPtransmitter(audio_device=device,
                                 ipv6=True,
                                 receiver_address=host,
                                 bitrate=int(settings.bitrate),
                                 opus_options=opus_options)
    transmitter.run()
    store.set('audio_caps', transmitter.caps)
    while store.get('lock_audio_stream') == 'true':
        Gst.Bus.poll(transmitter.pipeline.get_bus(), 0, 1)
        time.sleep(2)
    store.set('audio_caps', '')
    transmitter.pipeline.set_state(Gst.State.NULL)
    return True


@celery.task
def rtp_rx(host):
    device = device_init()
    settings = Settings.query.get(1)
    subprocess.call("sudo ip6tables -A INPUT -p udp --source '" +
                    host + "' -j ACCEPT", shell=True)
    get_caps = True
    while get_caps:
        time.sleep(2)
        try:
            request = http.request('GET', 'http://['+host+']/api1/audio_caps/')
            audio_caps_json = json.loads(request.data)
        except:
            pass
        else:
            if audio_caps_json['result']:
                get_caps = False
    caps = audio_caps_json['result']
    receiver = RTPreceiver(caps=caps,
                           audio_device=device,
                           transmitter_address=host,
                           ipv6=True,
                           bitrate=int(settings.bitrate),
                           jitter_buffer=int(settings.jitter))
    receiver.run()
    while store.get('lock_audio_stream') == 'true':
        Gst.Bus.poll(receiver.pipeline.get_bus(), 0, 1)
        time.sleep(2)
    receiver.pipeline.set_state(Gst.State.NULL)
    subprocess.call("sudo ip6tables -D INPUT -p udp --source '" +
                    host + "' -j ACCEPT", shell=True)
    return True


@celery.task
def play_audio():
    device = device_init()
    store.setex('lock_play_audio', 'true', '30')
    player = Play(audio_device=device)
    player.run()
    player.loop()
    store.setex('lock_play_audio', 'false', '30')
    return True


@celery.task
def system_shutdown():
    time.sleep(3)
    subprocess.call(["sudo", "halt"])
    return True


@celery.task
def system_reboot():
    time.sleep(3)
    subprocess.call(["sudo", "reboot"])
    return True


@celery.task
def api_peer_status(host):
    r = http.request('GET', 'http://['+host+']/api1/peer_status/')
    return True


@celery.task
def api_peer_invite(host):
    r = http.request('GET', 'http://['+host+']/api1/peers/')
    return True


@celery.task
def periodic_status_update():
    peers = Peer.query.all()
    for peer in peers:
        try:
            http.request('GET', 'http://['+peer.host+']/api1/peer_status/')
        except:
            pass
    return True
