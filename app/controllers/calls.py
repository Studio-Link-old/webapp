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
from app.models.accounts import Accounts
from app.forms.dial import DialForm
import time
import json
import requests
import urllib3
import redis

mod = Blueprint('calls', __name__, url_prefix='/calls')
http_small = urllib3.PoolManager(timeout=1)
store = redis.Redis('127.0.0.1')


@mod.route('/', methods=('GET', 'POST'))
def index():
    form = DialForm(request.form)
    ipv6 = ""
    try:
        ipv6 = http_small.request('GET', 'http://ipv6.studio-connect.de/').data
    except:
        pass

    db_accounts = Accounts.query.all()
    accounts = []
    if ipv6:
        accounts.append(('Local IPv6', 'Local IPv6'))

    for account in db_accounts:
        accounts.append((account.name, account.name))
    form.accounts.choices = accounts

    if form.validate_on_submit():
        try:
            r = requests.get('http://127.0.0.1:8000/?d')  # List active calls
        except:
            pass
        store.set('call_number', form.number.data)
        store.set('call_account', form.accounts.data)
        return redirect('/calls/dial')
    if form.errors:
        for error in form.errors:
            flash(error+': '+form.errors[error][0], 'danger')

    if not accounts and not ipv6:
        return render_template('calls/no_accounts.html')
    return render_template('calls/index.html', form=form, ipv6=ipv6)


@mod.route('/dial')
def dial():
    r = ""
    try:
        r = requests.get('http://127.0.0.1:8000/?l')  # List active calls
    except:
        pass
    return render_template('calls/dial.html',
                           call_number=store.get('call_number'),
                           call_account=store.get('call_account'),
                           baresip=r
                           )


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
