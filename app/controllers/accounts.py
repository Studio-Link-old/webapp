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
from app.forms.accounts import AddForm, EditForm
from app import tasks
from sqlalchemy.exc import IntegrityError
import urllib3

http_small = urllib3.PoolManager(timeout=1)
mod = Blueprint('accounts', __name__, url_prefix='/accounts')


@mod.route('/')
def index():
    ipv4 = ""
    ipv6 = ""
    try:
        #ipv4= http_small.request('GET', 'http://ipv4.studio-connect.de/').data
        ipv6 = http_small.request('GET', 'http://ipv6.studio-connect.de/').data
    except:
        pass
    accounts = Accounts.query.all()
    tasks.account_config.delay(accounts)
    return render_template("accounts/index.html", accounts=accounts, ipv4=ipv4,
                           ipv6=ipv6)


@mod.route('/add/', methods=('GET', 'POST'))
def add():
    form = AddForm(request.form)
    if form.validate_on_submit():
        account = Accounts(form.data)
        db.session.add(account)
        try:
            db.session.commit()
            return redirect(url_for('accounts.index'))
        except IntegrityError:
            flash(u'IntegrityError', 'danger')
    return render_template("accounts/form.html", form=form)


@mod.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    account = Accounts.query.get(id)
    password = account.password
    form = EditForm(obj=account)
    if form.validate_on_submit():
        form.populate_obj(account)
        if not request.form['password']:
            account.password = password
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('accounts.index'))
    return render_template("accounts/form.html",
                           form=form, action='/accounts/edit/'+id)


@mod.route('/delete/<id>')
def delete(id):
    db.session.delete(Accounts.query.get(id))
    db.session.commit()
    return redirect(url_for('accounts.index'))
