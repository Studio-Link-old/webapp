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


class Settings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(120), unique=True)
    codec = db.Column(db.String(120), unique=True)
    audio = db.Column(db.String(120), unique=True)
    complexity = db.Column(db.String(120), unique=True)
    bitrate = db.Column(db.String(120), unique=True)
    jitter = db.Column(db.String(120), unique=True)
    framesize = db.Column(db.String(120), unique=True)

    def __init__(self, device):
        self.device = device
        self.codec = "opus"
        self.audio = "music"
        self.complexity = "6"
        self.bitrate = "64000"
        self.jitter = "1-5"
        self.framesize = "20"
