from flask import Blueprint, render_template, redirect, request, url_for, flash

from app import db
from app.models.provider import Provider
from app.models.settings import Settings
from app.forms.settings import SettingsForm
from sqlalchemy.exc import IntegrityError

mod = Blueprint('settings', __name__, url_prefix='/settings')

@mod.route('/', methods=["GET","POST"])
def settings():
    """ show settings """
    settings = Settings.query.get(1)
    form = SettingsForm(request.form, obj=settings)

    if form.validate_on_submit():
        if settings:
            settings.device = form.device.data
            #db.session.merge(provider)
            db.session.commit()
            flash("Settings changed")
        else:
            settings = Settings(form.device.data)
            db.session.add(settings)
            db.session.commit()
            flash("Settings added")
    return render_template("settings.html", form=form)
