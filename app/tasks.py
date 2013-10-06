from __future__ import absolute_import
from app.celery import celery
from app.libs.audio.play import Play
from app.models.settings import Settings
from app.libs.rtp.rx import RTPreceiver
from app.libs.rtp.tx import RTPtransmitter
from gi.repository import Gst
import redis
import urllib3
import alsaaudio
import subprocess
import time

http = urllib3.PoolManager()
store = redis.Redis('127.0.0.1')


def device_init():
    settings = Settings.query.get(1)
    devices = alsaaudio.cards()
    idx = devices.index(settings.device)
    device = 'hw:' + str(idx)
    return device


@celery.task
def rtp_tx(host):
    device = device_init()
    transmitter = RTPtransmitter(audio_device=device, ipv6=True,
                                 receiver_address=host)
    transmitter.run()
    while store.get('lock_audio_stream') == 'true':
        Gst.Bus.poll(transmitter.pipeline.get_bus(), 0, 1)
        time.sleep(2)
    return True


@celery.task
def rtp_rx(host):
    device = device_init()
    subprocess.call("sudo ip6tables -A INPUT -p udp --source '" + host + "' -j ACCEPT", shell=True)
    caps = "application/x-rtp,media=(string)audio,clock-rate=(int)48000,encoding-name=(string)X-GST-OPUS-DRAFT-SPITTKA-00"
    receiver = RTPreceiver(caps=caps, audio_device=device, ipv6=True)
    receiver.run()
    while store.get('lock_audio_stream') == 'true':
        Gst.Bus.poll(receiver.pipeline.get_bus(), 0, 1)
        time.sleep(2)
    subprocess.call("sudo ip6tables -D INPUT -p udp --source '" + host + "' -j ACCEPT", shell=True)
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
    r = http.request('GET', 'http://['+host+']/api1/peer_status/')
    return True
