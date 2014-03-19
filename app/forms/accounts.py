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
from wtforms import TextField, SubmitField, PasswordField
from wtforms.validators import InputRequired


class AddForm(Form):
    name = TextField('Name', [InputRequired()])
    server = TextField('Server', [InputRequired()])
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    submit_button = SubmitField('Save')


class EditForm(Form):
    name = TextField('Name', [InputRequired()])
    server = TextField('Server', [InputRequired()])
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password')
    submit_button = SubmitField('Save')
