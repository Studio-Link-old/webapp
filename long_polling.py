#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()

import gevent
from gevent import pywsgi
from gevent import queue
import redis
import json


def process_messages(body):
    server = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=29)
    client = server.pubsub()
    client.subscribe('baresip_call_event')
    messages = client.listen()
    value = None

    while True:
	try:
	        message = messages.next()
	except:
		break

        event = message['data']
        print "%s" % event

        # With fallback if client misses the event (e.g. page reload)
        if event == 'INCOMING' or server.get('baresip_status') == 'INCOMING':
            value = server.get('baresip_peeruri');
            event = 'INCOMING'
            break

    if value:
        body.put(json.dumps({event: value}))
    else:
        body.put(json.dumps({}))
    body.put(StopIteration)
     

def handle(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = queue.Queue()
    body.put(' ' * 1000) # browser workaround
    gevent.spawn(process_messages, body)
    return body

server = pywsgi.WSGIServer(('127.0.0.1', 1234), handle)
print "Serving on http://127.0.0.1:1234..."
server.serve_forever()
