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

import requests
import redis
import socket

url = 'http://127.0.0.1:8000/?'


def get(cmd='list'):

    if cmd == 'list':
        return requests.get(url+'l').content
    elif cmd == 'reg_status':
        return requests.get(url+'r').content

    raise NameError('Baresip command not found')


def set(cmd='ua_next', data=''):

    if cmd == 'ua_next':
        return requests.get(url+'j').content
    elif cmd == 'answer':
        return requests.get(url+'f').content
    elif cmd == 'hangup':
        return requests.get(url+'b').content
    elif cmd == 'dial':
        sip = data
        if sip.find('@'):
            sip_user = sip.split('@')[0]
            sip_host = sip.split('@')[1]

            # testing ipv6 address
            try:
                socket.inet_pton(socket.AF_INET6, sip_host)
                sip = sip_user+'@['+sip_host+']'
            except socket.error:
                pass

        return requests.get(url+'d'+sip).content
    elif cmd == 'start_audio_loop':
        return requests.get(url+'a').content
    elif cmd == 'stop_audio_loop':
        return requests.get(url+'e').content

    raise NameError('Baresip command not found')
