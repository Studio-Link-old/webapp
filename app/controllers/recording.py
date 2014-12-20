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

mod = Blueprint('recording', __name__, url_prefix='/recording')


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
    return render_template('recording.html',mount_failed=mount_failed,files=files)

