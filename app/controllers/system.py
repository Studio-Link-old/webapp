from flask import Blueprint, request, flash, url_for, redirect
from app import tasks

mod = Blueprint('system', __name__, url_prefix='/system')


@mod.route('/shutdown')
def shutdown():  # pragma: no cover
    flash("Shutting down. When the LEDs on the board stop flashing, \
    it should be safe to unplug your Raspberry Pi.", "danger")
    tasks.system_shutdown.delay()
    return redirect(url_for('index'))


@mod.route('/reboot')
def reboot():  # pragma: no cover
    flash("Rebooting... please wait. This will take approx. one minute.", "danger")
    tasks.system_reboot.delay()
    return redirect(url_for('index'))
