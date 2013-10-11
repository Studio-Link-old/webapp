# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          ______                            __  |
# |  / ___// /___  ______/ (_)___     / ____/___  ____  ____  ___  _____/ /_ |
# |  \__ \/ __/ / / / __  / / __ \   / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/ |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ /_/ / / / / / / /  __/ /__/ /_   |
# |/____/\__/\__,_/\__,_/_/\____/   \____/\____/_/ /_/_/ /_/\___/\___/\__/   |
# |Copyright Sebastian Reimers 2013 studio-connect.de                        |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask import Blueprint, render_template, redirect, request, url_for, flash

from app import db
from app.models.settings import Settings
from app.forms.settings import SettingsForm
from sqlalchemy.exc import IntegrityError
import alsaaudio
import subprocess

mod = Blueprint('settings', __name__, url_prefix='/settings')


@mod.route('/', methods=["GET", "POST"])
def settings():
    """ show settings """
    settings = Settings.query.get(1)
    form = SettingsForm(request.form, obj=settings)
    devices = []
    raw_devices = alsaaudio.cards()
    for raw_device in raw_devices:
        devices.append((raw_device, raw_device))
    form.device.choices = devices

    if form.validate_on_submit():
        if settings:
            settings.device = form.device.data
            #db.session.merge(provider)
            db.session.commit()
            flash("Settings changed", "success")
        else:
            settings = Settings(form.device.data)
            db.session.add(settings)
            db.session.commit()
            flash("Settings added", "success")
    platform = subprocess.call(["uname", "-m"])
    return render_template("settings.html", form=form, platform=platform)
