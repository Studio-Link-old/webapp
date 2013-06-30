import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = "cH4ng3_M3"
BABEL_DEFAULT_LOCALE = "de"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}
