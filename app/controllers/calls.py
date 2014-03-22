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
from app.models.accounts import Accounts
from app.forms.dial import DialForm
import time
import json
import requests
import urllib3
import redis
import re

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
            r = requests.get('http://127.0.0.1:8000/?d'+form.number.data)
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
    r = "Could not connect to baresip."
    try:
        r = requests.get('http://127.0.0.1:8000/?l').content  # Active calls
    except:
        pass
    return render_template('calls/dial.html',
                           call_number=store.get('call_number'),
                           call_account=store.get('call_account'),
                           baresip=r
                           )

@mod.route('/accept')
def accept():
    try:
        r = requests.get('http://127.0.0.1:8000/?f').content
    except:
        return json.dumps({'return': False})
    return json.dumps({'return': True})


@mod.route('/dismiss')
def dismiss():
    try:
        r = requests.get('http://127.0.0.1:8000/?b').content
    except:
        return json.dumps({'return': False})
    return json.dumps({'return': True})


@mod.route('/events')
def events():
    key_timeout = '1800'
    event_procs = store.get('event_procs')
    if not event_procs:
        event_procs = 1
    else:
        event_procs = int(event_procs) + 1
    store.setex('event_procs', event_procs, key_timeout)

    # Long polling (timeout 20 seconds)
    count = 0
    while count < 10:
        time.sleep(1)

        # Limit processes
        event_procs = int(store.get('event_procs'))
        if event_procs >= 4:
            cleanup_events(key_timeout)
            return json.dumps({'LIMITED': True})

        # Get baresip status
        try:
            r = requests.get('http://127.0.0.1:8000/?l')  # Active calls
        except:
            pass
        else:
            cleanup_events(key_timeout)
            if 'INCOMING' in r.content:
                m = re.search('sip:.*@*.', r.content)
                return json.dumps({'INCOMING': m.group(0)})
            elif 'ESTABLISHED' in r.content:
                return json.dumps({'ESTABLISHED': True})
        count = count + 1
    cleanup_events(key_timeout)
    return json.dumps({})


def cleanup_events(key_timeout):
    event_procs = int(store.get('event_procs'))
    event_procs = event_procs - 1
    store.setex('event_procs', event_procs, key_timeout)
