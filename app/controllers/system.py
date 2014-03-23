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

from flask import Blueprint, request, flash, url_for, redirect, Response
from flask import render_template
from app import tasks
import psutil
import json
import subprocess

mod = Blueprint('system', __name__, url_prefix='/system')


@mod.route('/shutdown')
def shutdown():  # pragma: no cover
    flash('Shutting down. When the LEDs on the board stop flashing, \
    it should be safe to unplug.', 'danger')
    tasks.system_shutdown.delay()
    return redirect(url_for('index'))


@mod.route('/reboot')
def reboot():  # pragma: no cover
    flash('Rebooting... please wait. This will take approx. one minute.',
          'danger')
    tasks.system_reboot.delay()
    return redirect(url_for('index'))


@mod.route('/raw')
def raw():
    o = json.dumps({
        'cpuusage': psutil.cpu_percent(0),
        'netio':    psutil.network_io_counters(),
    })
    return Response(o, mimetype='application/json')

@mod.route('/log/<match>')
@mod.route('/log')
def log(match=False):
    if match == 'baresip':
        log = subprocess.check_output(['sudo', 'journalctl', '-n', '100',
                                      '-r', '/usr/bin/baresip'])
    else:
        log = subprocess.check_output(['sudo', 'journalctl', '-n', '100',
                                      '-r'])
    return render_template('log.html', log=log.decode('utf-8'))
