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

from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SubmitField, PasswordField
from wtforms.validators import Required, ValidationError

DEFAULT_CHOICES = []


class SettingsForm(Form):
    device = SelectField('Audio device', choices=DEFAULT_CHOICES)
    codec = SelectField('Codec', choices=[('opus', 'Opus'), ('pcm', 'PCM')],
                        default='opus')
    submit_button = SubmitField('Save')


class PasswordForm(Form):
    password = PasswordField('Password', [Required()])
    submit_button = SubmitField('Change password')
