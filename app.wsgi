from gevent.wsgi import WSGIServer
from app import app
from gevent import monkey
monkey.patch_all()

http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()
