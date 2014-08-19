# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          __    _       __                      |
# |  / ___// /___  ______/ (_)___     / /   (_)___  / /__                    |
# |  \__ \/ __/ / / / __  / / __ \   / /   / / __ \/ //_/                    |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ / / / / ,<                       |
# |/____/\__/\__,_/\__,_/_/\____/  /_____/_/_/ /_/_/|_|                      |
# |Copyright Sebastian Reimers 2013 - 2014 studio-link.de                    |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask import Blueprint, request, flash, url_for, redirect, Response
from flask import render_template
from app import tasks
from app.libs import baresip
import psutil
import json
import subprocess
import requests
import redis

mod = Blueprint('system', __name__, url_prefix='/system')
store = redis.Redis('127.0.0.1')


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
        cmd = 'sudo journalctl -r /usr/bin/baresip |\
               grep -v "ua: sip:" | head -100'
        log = subprocess.check_output(cmd, shell=True)
    else:
        log = subprocess.check_output('sudo journalctl -r | head -100',
                                      shell=True)
    return render_template('log.html', log=log.decode('utf-8'))


@mod.route('/update')
def update():
    url = 'http://studio-link.de/releases.json'
    r = requests.get(url)
    f = open('/etc/studio-release', 'r')
    current = f.read().rstrip()

    releases = []
    for release in r.json():
        if not release['prerelease']:
            releases.append(release['tag_name'])

    releases.sort()

    if current in releases:
        current_index = releases.index(current)
    else:
        current_index = len(releases)

    if current_index < len(releases)-1:
        next_release = releases[current_index+1]
        up2date = False
        store.set('next_release', next_release)
    else:
        next_release = current
        up2date = True

    return render_template('update.html',
                           up2date=up2date,
                           next_release=next_release)


@mod.route('/upgrade/<version>')
@mod.route('/upgrade')
def upgrade(version=False):
    if version:
        store.set('next_release', version)
    tasks.upgrade.delay()
    return render_template('upgrade.html')


@mod.route('/info')
def info():
    cmd = "ip link show eth0 | grep ether | awk '{ print $2 }'"
    provisioning = subprocess.check_output(cmd, shell=True)
    info = baresip.get('system_info')

    return render_template('info.html', info=info, provisioning=provisioning)
