# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          __    _       __                      |
# |  / ___// /___  ______/ (_)___     / /   (_)___  / /__                    |
# |  \__ \/ __/ / / / __  / / __ \   / /   / / __ \/ //_/                    |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ / / / / ,<                       |
# |/____/\__/\__,_/\__,_/_/\____/  /_____/_/_/ /_/_/|_|                      |
# |Copyright Sebastian Reimers 2013 - 2015 studio-link.de                    |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask_wtf import Form
from wtforms import TextField, SubmitField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired


class AddForm(Form):
    name = TextField('Name', [InputRequired()])
    server = TextField('Server', [InputRequired()])
    transport = SelectField('Transport',
                             choices=[('udp', 'UDP'),
                                      ('tcp', 'TCP'),
                                      ('tls', 'TLS')],
                             default='udp')
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    answermode = SelectField('Answermode',
                             choices=[('manual', 'Manual'),
                                      ('auto', 'Auto')],
                             default='manual')
    submit_button = SubmitField('Save')


class EditForm(Form):
    name = TextField('Name', [InputRequired()])
    server = TextField('Server', [InputRequired()])
    transport = SelectField('Transport',
                             choices=[('udp', 'UDP'),
                                      ('tcp', 'TCP'),
                                      ('tls', 'TLS')],
                             default='udp')
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password')
    answermode = SelectField('Answermode',
                             choices=[('manual', 'Manual'),
                                      ('auto', 'Auto')],
                             default='manual')
    codecs = SelectMultipleField('Codecs',
                                 choices=[('opus/48000/2', 'Opus 48kHz Stereo'),
                                          ('opus/48000/1', 'Opus 48kHz Mono'),
                                          ('G722', 'G.722 16kHz'),
                                          ('G726-40/8000/1', 'G.726-40 8kHz'),
                                          ('PCMU', 'G.711u 8kHz'),
                                          ('PCMA', 'G.711a 8kHz'),
                                          ('GSM', 'GSM 8kHz'),
                                          ('L16', 'PCM 48kHz')])

    submit_button = SubmitField('Save')


class EditProvisioningForm(Form):
    name = TextField('Name', [InputRequired()])
    answermode = SelectField('Answermode',
                             choices=[('manual', 'Manual'),
                                      ('auto', 'Auto')],
                             default='manual')
    codecs = SelectMultipleField('Codecs',
                                 choices=[('opus/48000/2', 'Opus 48kHz Stereo'),
                                          ('opus/48000/1', 'Opus 48kHz Mono')])
    submit_button = SubmitField('Save')
