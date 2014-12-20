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

mod = Blueprint('recording', __name__, url_prefix='/recording')


@mod.route('/index')
def index():

    mount_failed = False
    try:
        subprocess.check_call("sudo mount | grep media | grep mmc", shell=True)
    except subprocess.CalledProcessError, e:
        mount_failed = True

    mount_status = False
    if not mount_failed:
        mount_status = True

    return render_template('recording.html',mount_status=mount_status)
