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


@app.before_request
def before_request():
    if store.get('oncall') == 'true':
        g.oncall = True
    else:
        g.oncall = False


@app.route('/')
def index():
    p = Popen('uptime', stdout=PIPE, stderr=STDOUT, close_fds=True)
    uptime = p.stdout.read()
    return render_template('index.html', uptime=uptime)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
