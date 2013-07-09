from __future__ import absolute_import

from app.celery import celery

from app.libs.audio.play import Play

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
    player = Play()
    player.run()
    player.loop()
    return True
