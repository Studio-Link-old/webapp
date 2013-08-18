# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy
from subprocess import Popen, PIPE, STDOUT

app = Flask(__name__)
app.config.from_object('config')

# Bootstrap init
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = True

# Babel init
Babel(app)

# SQL Alchemy init
db = SQLAlchemy(app)

# Import blueprints
from app.controllers.system import mod as systemModule
app.register_blueprint(systemModule)

from app.controllers.mixers import mod as mixersModule
app.register_blueprint(mixersModule)

from app.controllers.peers import mod as peersModule
app.register_blueprint(peersModule)

from app.controllers.api import mod as apiModule
app.register_blueprint(apiModule)


@app.route('/')
def index():
    p = Popen('uptime', stdout=PIPE, stderr=STDOUT, close_fds=True)
    uptime = p.stdout.read()
    return render_template('index.html', uptime=uptime)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
