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
import socket


def check_ipv6(form, field):
    try:
        socket.inet_pton(socket.AF_INET6, field.data)
        return True
    except socket.error:
        raise ValidationError('Not a valid IPv6 address!')


class AddForm(Form):
    name = TextField('Name', [Required()])
    host = TextField('Host IPv6', [Required(), check_ipv6])
    submit_button = SubmitField('Save')


class EditForm(Form):
    name = TextField('Name', [Required()])
    submit_button = SubmitField('Save')

