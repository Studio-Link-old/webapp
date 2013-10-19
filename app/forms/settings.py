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

from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SubmitField
from wtforms.validators import Required, ValidationError

DEFAULT_CHOICES = []


class SettingsForm(Form):
    device = SelectField('Audio device', choices=DEFAULT_CHOICES)
    codec = SelectField('Codec', choices=[('opus', 'Opus'), ('pcm', 'PCM')], default='opus')
    audio = SelectField('Audio',
                        choices=[('voice', 'Voice'), ('music', 'Music')])
    complexity = SelectField('Complexity', choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ], default='10')
    bitrate = SelectField('Bitrate (kbit/s)', choices=[
        ('192', '192'),
        ('128', '128'),
        ('96', '96'),
        ('64', '64'),
        ('48', '48'),
        ('32', '32'),
        ('24', '24'),
        ('16', '16'),
        ], default='64')
    jitter = SelectField('Jitter', choices=[
        ('300', '300ms'),
        ('250', '250ms'),
        ('200', '200ms'),
        ('150', '150ms'),
        ('100', '100ms'),
        ('50', '50ms'),
        ('25', '25ms'),
        ('10', '10ms'),
        ], default='150')
    framesize = SelectField('Framesize', choices=[
        ('60', '60ms'),
        ('40', '40ms'),
        ('20', '20ms'),
        ('10', '10ms'),
        ('5', '5ms'),
        ('2', '2ms'),
        ], default='20')
    submit_button = SubmitField('Save')
