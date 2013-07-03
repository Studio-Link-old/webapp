from __future__ import absolute_import

from app.celery import celery

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
