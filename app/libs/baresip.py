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

from flask import flash
import requests
import socket
import re


def curl(param):
    url = 'http://127.0.0.1:8000/?'
    try:
        content = requests.get(url+param).content
    except:
        flash('baresip connection problem', 'danger')
        content = ''
    return content


def get(cmd='list', query=''):

    if cmd == 'list':
        return curl('l')

    elif cmd == 'reg_status':
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

    raise NameError('Baresip command not found')


def set(cmd='ua_next', data=''):

    if cmd == 'ua_next':
        return curl('j')

    elif cmd == 'answer':
        return curl('f')

    elif cmd == 'hangup':
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

    elif cmd == 'start_audio_loop':
        return curl('a')

    elif cmd == 'stop_audio_loop':
        return curl('e')

    raise NameError('Baresip command not found')
