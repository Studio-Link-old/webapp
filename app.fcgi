#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/tmp/fcgi.sock', umask=0).run()
