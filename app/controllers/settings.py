# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          __    _       __                      |
# |  / ___// /___  ______/ (_)___     / /   (_)___  / /__                    |
# |  \__ \/ __/ / / / __  / / __ \   / /   / / __ \/ //_/                    |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ / / / / ,<                       |
# |/____/\__/\__,_/\__,_/_/\____/  /_____/_/_/ /_/_/|_|                      |
# |Copyright Sebastian Reimers 2013 - 2015 studio-link.de                    |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask import Blueprint, render_template, redirect, request, url_for, flash

from app import db
from app.models.settings import Settings
from app.forms.settings import SettingsForm, PasswordForm
from sqlalchemy.exc import IntegrityError
from subprocess import call
from app import tasks
import alsaaudio
import htpasswd

mod = Blueprint('settings', __name__, url_prefix='/settings')


@mod.route('/', methods=['GET', 'POST'])
def settings():
    """ show settings """
    settings = Settings.query.get(1)
    form = SettingsForm(request.form, obj=settings)
    devices = []
    raw_devices = alsaaudio.cards()
    for raw_device in raw_devices:
        devices.append((raw_device, raw_device))
    form.device.choices = devices

    form_password = PasswordForm(request.form)

    if form.validate_on_submit():
        new_password = str(form_password.password.data)
        if new_password:
            call("echo 'studio:" + new_password + "' | sudo chpasswd",
                 shell=True)
            with htpasswd.Basic('/opt/studio/webapp/htpasswd') as userdb:
                try:
                    userdb.change_password('studio', new_password)
                except htpasswd.basic.UserNotExists, e:
                    print e
            flash('Password changed', 'success')
        else:
            if settings:
                form.populate_obj(settings)
                db.session.commit()
                flash('Settings changed', 'success')
            else:
                settings = Settings(form.device.data)
                db.session.add(settings)
                db.session.commit()
                flash('Settings added', 'success')
            # Generate baresip config
            tasks.baresip_config.delay()
            tasks.account_config.delay()

    return render_template('settings.html', form=form,
                           form_password=form_password)
