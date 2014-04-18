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

from flask_wtf import Form
from wtforms import TextField, SelectField, SubmitField, PasswordField
from wtforms.validators import Required, ValidationError

DEFAULT_CHOICES = []


class SettingsForm(Form):
    device = SelectField('Audio device', choices=DEFAULT_CHOICES)
    codec = SelectField('Preferred codec',
                        choices=[('opus', 'Opus 48kHz'),
                                 ('g722', 'G.722 16kHz'),
                                 ('g726', 'G.726 8kHz'),
                                 ('g711', 'G.711 8kHz'),
                                 ('gsm', 'GSM 8kHz'),
                                 ('l16', 'PCM 48kHz')],
                        default='opus')
    jitter = SelectField('Jitterbuffer',
                         choices=[('1-5', 'Small (1-5 frames)'),
                                  ('5-10', 'Big (5-10 frames)')],
                         default='1-5')
    submit_button = SubmitField('Save')


class PasswordForm(Form):
    password = PasswordField('Password', [Required()])
    submit_button = SubmitField('Change password')
