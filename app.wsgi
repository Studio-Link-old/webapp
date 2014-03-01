from gevent.wsgi import WSGIServer
from app import app
from gevent import monkey
from gevent import socket
import os
monkey.patch_all()

listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sockname = '/tmp/wsgi.sock'
if os.path.exists(sockname):
    os.remove(sockname)
listener.bind(sockname)
listener.listen(1)
http_server = WSGIServer(listener, app)
http_server.serve_forever()
