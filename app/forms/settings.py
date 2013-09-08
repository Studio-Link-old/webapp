from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import Required, ValidationError

class SettingsForm(Form):
        rssfeed = TextField('rssfeed', [Required()])
