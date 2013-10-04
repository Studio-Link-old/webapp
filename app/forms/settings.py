from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SubmitField
from wtforms.validators import Required, ValidationError

DEFAULT_CHOICES = []


class SettingsForm(Form):
    device = SelectField('Audio device', choices=DEFAULT_CHOICES)
    submit_button = SubmitField('Save')
