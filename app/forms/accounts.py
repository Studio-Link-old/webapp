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
from wtforms import TextField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired


class AddForm(Form):
    name = TextField('Name', [InputRequired()])
    server = TextField('Server', [InputRequired()])
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
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password')
    answermode = SelectField('Answermode',
                             choices=[('manual', 'Manual'),
                                      ('auto', 'Auto')],
                             default='manual')
    submit_button = SubmitField('Save')


class EditProvisioningForm(Form):
    name = TextField('Name', [InputRequired()])
    password = PasswordField('Password')
    answermode = SelectField('Answermode',
                             choices=[('manual', 'Manual'),
                                      ('auto', 'Auto')],
                             default='manual')
    submit_button = SubmitField('Save')
