from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import Required, ValidationError
import alsaaudio


class SettingsForm(Form):
    devices = []
    raw_devices = alsaaudio.cards()
    for raw_device in raw_devices:
        devices.append((raw_device, raw_device))
    device = SelectField('Audio device', choices=devices)
