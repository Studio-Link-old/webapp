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

from flask import Blueprint, request, flash, url_for, redirect, Response
from flask import render_template
import jack
import subprocess

mod = Blueprint('routing', __name__, url_prefix='/routing')


@mod.route('/index')
def index():
    try:
        ports = jack.get_ports()
    except jack.NotConnectedError:
        jack.attach('studio-webapp')
        ports = jack.get_ports()

    inports = []
    outports = []
    connects = {}

    for port in ports:
        if (jack.get_port_flags(port) & jack.IsInput) > 0:
            inports.append(port)
            connects[port] = jack.get_connections(port)
        if (jack.get_port_flags(port) & jack.IsOutput) > 0:
            outports.append(port)

    otg_systemd_status = subprocess.check_output(['sudo', 'systemctl', 'is-active', 'studio-otg'])
    if otg_systemd_status == 'active':
        otg_status = True
    else:
        otg_status = False

    return render_template('routing.html', inports=inports, outports=outports,
                           connects=connects, otg_status=otg_status)


@mod.route('/route/<source>/<destination>')
def route(source, destination):
    try:
        jack.connect(source, destination)
    except jack.NotConnectedError:
        jack.attach("studio-webapp")
        jack.connect(source, destination)

    return ''


@mod.route('/unroute/<source>/<destination>')
def unroute(source, destination):
    try:
        jack.disconnect(source, destination)
    except jack.NotConnectedError:
        jack.attach("studio-webapp")
        jack.disconnect(source, destination)

    return ''


@mod.route('/otg/<status>')
def otg(status):
    if status == 'true':
        subprocess.call(['sudo', 'systemctl', 'enable', 'studio-otg'])
        subprocess.call(['sudo', 'systemctl', 'start', 'studio-otg'])
    else:
        subprocess.call(['sudo', 'systemctl', 'disable', 'studio-otg'])
        subprocess.call(['sudo', 'systemctl', 'stop', 'studio-otg'])

    return redirect(url_for('routing.index'))
