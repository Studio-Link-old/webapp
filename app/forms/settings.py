# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          __    _       __                      |
# |  / ___// /___  ______/ (_)___     / /   (_)___  / /__                    |
# |  \__ \/ __/ / / / __  / / __ \   / /   / / __ \/ //_/                    |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ / / / / ,<                       |
# |/____/\__/\__,_/\__,_/_/\____/  /_____/_/_/ /_/_/|_|                      |
# |Copyright Sebastian Reimers 2013 - 2014 studio-link.de                    |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask_wtf import Form
from wtforms import TextField, SelectField, SubmitField, PasswordField
from wtforms.validators import Required, ValidationError

DEFAULT_CHOICES = []


class SettingsForm(Form):
    device = SelectField('Audio device', choices=DEFAULT_CHOICES)

    audio = SelectField('Soundsystem',
                         choices=[('alsa', 'ALSA'),
                                  ('jack', 'JACK (beta)')],
                         default='alsa')

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

    bitrate = SelectField('Opus Bitrate (kbit/s)', choices=[
        ('192000', '192'),
        ('128000', '128'),
        ('96000', '96'),
        ('64000', '64'),
        ('48000', '48'),
        ('32000', '32'),
        ('24000', '24'),
        ('16000', '16'),
        ], default='64')

    framesize = SelectField('Framesize', choices=[
        ('60', '60ms'),
        ('40', '40ms'),
        ('20', '20ms'),
        ('10', '10ms'),
        ('5', '5ms'),
        ], default='20')

    submit_button = SubmitField('Save')


class PasswordForm(Form):
    password = PasswordField('Password', [Required()])
    submit_button = SubmitField('Change password')
