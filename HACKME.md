# Hackme - Howto contribute

## Install requirements

`pip install -r requirements.txt`


## Translation

`$ pybabel extract -F babel.cfg -o messages.pot .`

`$ pybabel update -i messages.pot -d translations`

Afterwards some strings might be marked as fuzzy (where it tried to figure out if a translation matched a changed key). If you have fuzzy entries, make sure to check them by hand and remove the fuzzy flag before compiling.

`$ pybabel compile -d translations`


## Init Database

`$ python -c "from app import db; db.create_all();"`

## Check pep8 style guide

`$ pip install pep8`

`$ pep8 --first app`


## Pylint

`$ pylint -E app`

`$ pylint -d all -e unused-import -r no app`


## Check coverage

`$ pip install nose`

`$ pip install coverage`

`$ nosetests --with-coverage --cover-html --cover-html-dir=../coverage --cover-package=app unittests.py`


## SQLAlchemy Migrations with Alembic

http://mattupstate.com/python/databases/2012/11/15/database-migrations-with-alembic-sqlalchemy-and-flask.html


```
$ alembic init alembic
$ alembic revision --autogenerate -m "Added some table"
$ alembic upgrade head
```
