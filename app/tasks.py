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
from jinja2 import Environment, FileSystemLoader
import alsaaudio
import redis
import subprocess
import time
import os

store = redis.Redis('127.0.0.1')
env = Environment(loader=FileSystemLoader('app/templates'))


def get_device():
    settings = Settings.query.get(1)
    devices = alsaaudio.cards()
    idx = devices.index(settings.device)
    device = 'plughw:' + str(idx) + ',0'
    return device


@celery.task
def account_config(accounts):
    template = env.get_template('config/baresip_accounts.cfg')
    output_from_parsed_template = template.render(accounts=accounts)

    with open(os.getenv('HOME') + '/.baresip/accounts', 'wb') as fh:
        fh.write(output_from_parsed_template)

    subprocess.call(['sudo', 'systemctl', 'restart', 'baresip'])


@celery.task
def baresip_config(settings):
    codecs = ['opus', 'g722', 'g726', 'g711', 'gsm', 'l16']
    codecs.remove(settings.codec)
    template = env.get_template('config/baresip.cfg')
    output_from_parsed_template = template.render(settings=settings,
                                                  codecs=codecs,
                                                  device=get_device())

    with open(os.getenv('HOME') + '/.baresip/config', 'wb') as fh:
        fh.write(output_from_parsed_template)

    subprocess.call(['sudo', 'systemctl', 'restart', 'baresip'])


@celery.task
def system_shutdown():
    time.sleep(3)
    subprocess.call(['sudo', 'systemctl', 'poweroff'])
    return True


@celery.task
def system_reboot():
    time.sleep(3)
    subprocess.call(['sudo', 'systemctl', 'reboot'])
    return True
