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
from app import db
from app.celery import celery
from app.models.settings import Settings
from app.models.accounts import Accounts
from jinja2 import Environment, FileSystemLoader
import alsaaudio
import redis
import subprocess
import time
import os
import csv

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
    settings = Settings.query.get(1)
    template = env.get_template('config/baresip_accounts.cfg')
    output_from_parsed_template = template.render(accounts=accounts,
                                                  ptime=settings.framesize)

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


@celery.task
def upgrade():
    time.sleep(3)
    subprocess.call(['sudo', 'systemctl', 'start', 'studio-update'])
    return True


@celery.task
def provisioning():
    # Delete old provisioning accounts
    db.session.query(Accounts).filter(Accounts.provisioning==True).delete()
    db.session.commit()

    # Add new accounts
    reader = csv.reader(open('/tmp/provisioning.txt', 'rb'), delimiter=';')
    for row in reader:
        account = Accounts({})
        account.name = row[0]
        account.username = row[1]
        account.password = row[2]
        account.server = row[3]
        account.options = row[4]
        account.provisioning = True
        db.session.add(account)
        db.session.commit()

    return True

