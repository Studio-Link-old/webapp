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
from app.libs import baresip
import time
import json
import redis
import re

mod = Blueprint('calls', __name__, url_prefix='/calls')
store = redis.Redis('127.0.0.1')


@mod.route('/', methods=('GET', 'POST'))
def index():
    form = DialForm(request.form)
    db_accounts = Accounts.query.all()
    accounts = []
    ipv6 = baresip.get('ipv6')
    if ipv6:
        accounts.append(('Local IPv6', 'Local IPv6'))

    for account in db_accounts:
        accounts.append((account.name, account.name))
    form.accounts.choices = accounts

    if form.validate_on_submit():
        baresip.set('dial', form.number.data)
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
    return render_template('calls/dial.html',
                           call_number=store.get('call_number'),
                           call_account=store.get('call_account'),
                           baresip=baresip.get('list')
                           )


@mod.route('/answer')
def answer():
    baresip.set('answer')
    store.set('oncall', 'true')
    return json.dumps({'return': True})


@mod.route('/hangup')
def hangup():
    baresip.set('hangup')
    store.set('oncall', 'false')
    return redirect('/calls/')


@mod.route('/events')
def events():
    accounts = int(Accounts.query.count()) + 1
    event_procs = store.get('event_procs')
    if not event_procs:
        event_procs = 1
    else:
        event_procs = int(event_procs) + 1
    store.setex('event_procs', event_procs, 60)

    # Long polling (timeout 20 seconds)
    count = 0
    while count < 20:
        time.sleep(1)

        # Limit processes
        event_procs = int(store.get('event_procs'))
        if event_procs >= 3:
            cleanup_events()
            return json.dumps({'LIMITED': True})

        # Get baresip call status (multi accounts)
        for account in range(0, accounts):
            call_list = baresip.get('list')

            if 'INCOMING' in call_list:
                m = re.search('sip:.*@*.', call_list)
                cleanup_events()
                return json.dumps({'INCOMING': m.group(0)})
            elif 'ESTABLISHED' in call_list:
                store.set('oncall', 'true')
                # Call is active we can sleep a little bit more
                time.sleep(5)
                cleanup_events()
                return json.dumps({'ESTABLISHED': True})

            # HINT: periodically switching user agent, is only a hack!!!
            # this is really bad if something else needs to select
            # a fix UA. At the moment its enough to switch at the and
            # of the loop. But multi call handling is not possible! The
            # first UA matched wins!
            baresip.set('ua_next')
        count = count + 1

        # If no UA matched a call, there is no call ;-)
        # This helps to detect a canceld call from peer
        store.set('oncall', 'false')
    cleanup_events()
    return json.dumps({})


def cleanup_events(key_timeout=60):
    event_procs = int(store.get('event_procs')) - 1
    store.setex('event_procs', event_procs, key_timeout)
