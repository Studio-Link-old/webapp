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

from flask import Blueprint, render_template, redirect, request, url_for, flash
from app import db
import time
import json
import requests

mod = Blueprint('calls', __name__, url_prefix='/calls')


@mod.route('/')
def index():
    return render_template('calls/index.html')


@mod.route('/dial')
def dial():
    return render_template('calls/index.html')


@mod.route('/events')
def events():
    count = 0
    # Long polling
    # @TODO: limit concurrent processes (max. 8), if reached quit the oldest
    while count < 20:
        time.sleep(1)
        try:
            r = requests.get('http://127.0.0.1:8000/?l')  # List active calls
        except:
            pass
        else:
            if 'INCOMING' in r.content:
                return json.dumps({'INCOMING': True})
            elif 'ESTABLISHED' in r.content:
                return json.dumps({'ESTABLISHED': True})
        count = count + 1
    return json.dumps({})
