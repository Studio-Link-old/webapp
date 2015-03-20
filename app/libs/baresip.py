# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          __    _       __                      |
# |  / ___// /___  ______/ (_)___     / /   (_)___  / /__                    |
# |  \__ \/ __/ / / / __  / / __ \   / /   / / __ \/ //_/                    |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ / / / / ,<                       |
# |/____/\__/\__,_/\__,_/_/\____/  /_____/_/_/ /_/_/|_|                      |
# |Copyright Sebastian Reimers 2013 - 2015 studio-link.de                    |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from flask import flash
from app.models.accounts import Accounts
import requests
import socket
import re


def curl(param):
    url = 'http://127.0.0.1:8000/raw/?'
    try:
        content = requests.get(url+param).content
    except:
        flash('baresip connection problem - please review <a href="/settings">settings</a>', 'danger')
        content = ''
    return content


def get(cmd='list', query=''):

    if cmd == 'list':
        return curl('l')

    elif cmd == 'call_active':
        calls = curl('c')
        empty_calls = re.search('no active calls', calls)
        if empty_calls:
            return False
        return True

    elif cmd == 'reg_status':
        # Workaround empty calls but no registrations
        if not get('call_active'):
            set("hangup")

        reg_status = curl('r')
        match = re.search(query + '.*(OK|ERR)', reg_status)
        if not match:
            return False
        else:
            if 'OK' in match.group(1):
                return True
            else:
                return False

    elif cmd == 'network':
        network_debug = curl('n')
        try:
            match = re.search(query + '.*-\ (.*)', network_debug)
            if not match:
                return None
            else:
                ipv6 = match.group(1)
        except IndexError:
            return None
        return ipv6

    elif cmd == 'ua_agent':
        return curl('u')

    elif cmd == 'system_info':
        return curl('s')

    raise NameError('Baresip command not found')


def set(cmd='ua_next', data=''):

    if cmd == 'ua_next':
        return curl('T')

    if cmd == 'user_agent':
        accounts = int(Accounts.query.count()) + 1
        for account in range(0, accounts):
            match = re.search(data, get('ua_agent'))
            if match:
                return True
            set('ua_next')
        return False

    elif cmd == 'answer':
        set('user_agent', data)
        return curl('D')

    elif cmd == 'hangup':
        set('user_agent', data)
        return curl('b')

    elif cmd == 'dial':
        sip = data
        if '@' in sip:
            sip_user = sip.split('@')[0]
            sip_host = sip.split('@')[1]

            # testing ipv6 address
            try:
                socket.inet_pton(socket.AF_INET6, sip_host)
                sip = sip_user+'@['+sip_host+']'
            except socket.error:
                pass

        return curl('d'+sip)

    elif cmd == 'audio_stream':
        return curl('a')

    raise NameError('Baresip command not found')
