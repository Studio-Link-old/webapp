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
    accounts.append(('studio@lan', 'Local'))

    for account in db_accounts:
        sip = account.username + '@' + account.server
        accounts.append((sip, account.name))
    form.accounts.choices = accounts

    if form.validate_on_submit():
        baresip.set('user_agent', form.accounts.data)
        baresip.set('dial', form.number.data)
        store.set('call_account', form.accounts.data)
        return redirect('/calls/dial')
    if form.errors:
        for error in form.errors:
            flash(error+': '+form.errors[error][0], 'danger')

    call_account = store.get('call_account')
    if call_account:
        form.accounts.data = call_account

    return render_template('calls/index.html', form=form)


@mod.route('/dial')
def dial():
    return render_template('calls/dial.html',
                           call_number=store.get('call_number'),
                           call_account=store.get('call_account'),
                           baresip=baresip.get('list')
                           )


@mod.route('/answer')
def answer():
    baresip.set('answer', store.get('baresip_ua'))
    store.set('oncall', 'true')
    store.set('baresip_status', 'ACCEPTED')
    store.set('oncalltext', 'CALL: ACCEPTED')
    return json.dumps({'return': True})


@mod.route('/hangup')
def hangup():
    agent = store.get('baresip_ua')
    if not agent:
        agent = store.get('call_account')
    baresip.set('hangup', agent)
    store.set('oncall', 'false')
    store.set('baresip_status', '')
    return redirect('/calls/')
