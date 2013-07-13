from __future__ import absolute_import
from app.celery import celery
from app.libs.audio.play import Play
import redis
import requests

@celery.task
def add(x, y):
    return x + y

@celery.task
def sync_peers():
    return True

@celery.task
def rtp_tx():
    return True

@celery.task
def rtp_rx():
    return True

@celery.task
def play_audio():
    store = redis.Redis('127.0.0.1')
    store.set('lock_play_audio', 'true', '30')
    player = Play()
    player.run()
    player.loop()
    store.set('lock_play_audio', 'false', '30')
    return True

@celery.task
def api_peer_status(host):
    requests.get('http://['+host+']/api1/peer_status')
    return True

@celery.task
def api_peer_invite(host):
    payload = {'name': 'value1', 'host': '::33'}
    requests.post('http://['+host+']/api1/peer_status', params=payload)
    return True
