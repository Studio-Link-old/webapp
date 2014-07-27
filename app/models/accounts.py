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

from app import db


class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    server = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))
    transport = db.Column(db.String(5))
    ptime = db.Column(db.String(3))
    options = db.Column(db.String(255))
    provisioning = db.Column(db.Boolean)
    answermode = db.Column(db.String(20))

    def __init__(self, form):
        self.transport = 'udp'  # possible udp/tcp/tls
        self.ptime = 20
        self.provisioning = False
        self.answermode = 'manual'  # {manual,early,auto}
        self.options = ''
        for var in form:
            setattr(self, var, form[var])
