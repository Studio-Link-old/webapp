# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          ______                            __  |
# |  / ___// /___  ______/ (_)___     / ____/___  ____  ____  ___  _____/ /_ |
# |  \__ \/ __/ / / / __  / / __ \   / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/ |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ /_/ / / / / / / /  __/ /__/ /_   |
# |/____/\__/\__,_/\__,_/_/\____/   \____/\____/_/ /_/_/ /_/\___/\___/\__/   |
# |Copyright Sebastian Reimers 2013 - 2014 studio-connect.de                 |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from __future__ import absolute_import
from app.celery import celery
from app.models.settings import Settings
import redis
import urllib3
import alsaaudio
import subprocess
import time
import json

http = urllib3.PoolManager(timeout=3)
store = redis.Redis('127.0.0.1')


@celery.task
def play_audio():
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
