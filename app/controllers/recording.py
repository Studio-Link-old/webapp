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
import subprocess
import glob
import time
import os.path
import redis

mod = Blueprint('recording', __name__, url_prefix='/recording')
store = redis.Redis('127.0.0.1')


@mod.route('/index')
def index():

    mount_failed = False
    files = {}

    try:
        subprocess.check_call("sudo mount | grep media | grep mmc", shell=True)
    except subprocess.CalledProcessError, e:
        mount_failed = True

    if not mount_failed:
        for flac_file in glob.glob('/media/*.flac'):
            ctime = time.strftime('%d.%m.%Y', time.gmtime(os.path.getmtime(flac_file)))
            total_samples = subprocess.check_output("metaflac --show-total-samples "+flac_file, shell=True)
            duration_min = int(total_samples) / 48000 / 60
            duration_sec = (int(total_samples) / 48000) - (duration_min * 60)
            duration_min_str = str(duration_min).zfill(2)
            duration_sec_str = str(duration_sec).zfill(2)
            files[flac_file[7:]] = {'date': ctime, 'duration_min': duration_min_str, 'duration_sec': duration_sec_str}

    try:
        capture_systemd_status = subprocess.check_output(['sudo',
                                                          'systemctl',
                                                          'is-active',
                                                          'studio-capture'])
    except subprocess.CalledProcessError, e:
        capture_systemd_status = 'failed'

    if capture_systemd_status == 'active\n':
        capture_status = True
    else:
        capture_status = False

    return render_template('recording.html',mount_failed=mount_failed,
                                            files=files,
                                            capture_status=capture_status,
                                            playback=store.get('playback'))


@mod.route('/start')
def start():
    subprocess.call(['sudo', 'systemctl', 'start', 'studio-capture'])
    return redirect(url_for('recording.index'))

@mod.route('/stop')
def stop():
    subprocess.call(['sudo', 'systemctl', 'stop', 'studio-capture'])
    return redirect(url_for('recording.index'))

@mod.route('/start_play/<filename>')
def start_play(filename):
    store.set('playback', filename)
    subprocess.call(['sudo', 'systemctl', 'start', 'studio-playback'])
    return redirect(url_for('recording.index'))

@mod.route('/stop_play')
def stop_play():
    store.set('playback', 'empty')
    subprocess.call(['sudo', 'systemctl', 'stop', 'studio-playback'])
    return redirect(url_for('recording.index'))

@mod.route('/delete/<filename>')
def delete(filename):
    subprocess.call(['rm', '/media/'+filename])
    return redirect(url_for('recording.index'))
