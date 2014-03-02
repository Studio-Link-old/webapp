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
import alsaaudio
import subprocess
import time
import json
import os
from jinja2 import Environment, FileSystemLoader

store = redis.Redis('127.0.0.1')
env = Environment(loader=FileSystemLoader('app/templates'))


@celery.task
def account_config(accounts):
    template = env.get_template('config/baresip_accounts.cfg')
    output_from_parsed_template = template.render(accounts=accounts)

    # to save the results
    with open(os.getenv('HOME') + "/.baresip/accounts", "wb") as fh:
        fh.write(output_from_parsed_template)

    subprocess.call(["sudo", "systemctl", "restart", "baresip"])


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
