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

from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from subprocess import Popen, PIPE, STDOUT
import redis

store = redis.Redis('127.0.0.1')
app = Flask(__name__, static_folder='templates/static')
app.config.from_object('config')

# Bootstrap init
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# Babel init
Babel(app)

# SQL Alchemy init
db = SQLAlchemy(app)

# Import blueprints
from app.controllers.system import mod as systemModule
app.register_blueprint(systemModule)

from app.controllers.mixers import mod as mixersModule
app.register_blueprint(mixersModule)

from app.controllers.accounts import mod as accountsModule
app.register_blueprint(accountsModule)

from app.controllers.calls import mod as callsModule
app.register_blueprint(callsModule)

from app.controllers.settings import mod as settingsModule
app.register_blueprint(settingsModule)

from app.controllers.routing import mod as routingModule
app.register_blueprint(routingModule)

from app.controllers.recording import mod as recordingModule
app.register_blueprint(recordingModule)


@app.before_request
def before_request():
    if store.get('oncall') == 'true':
        g.oncall = True
        g.oncalltext = store.get('oncalltext')
    else:
        g.oncall = False

    if store.get('reboot_required') == 'true':
        g.reboot_required = True
    else:
        g.reboot_required = False


@app.route('/')
def index():
    p = Popen('uptime', stdout=PIPE, stderr=STDOUT, close_fds=True)
    uptime = p.stdout.read()
    return render_template('index.html', uptime=uptime)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
