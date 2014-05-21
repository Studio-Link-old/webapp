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
