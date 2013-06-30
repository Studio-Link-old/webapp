# Hackme - Howto contribute

## Translation

`$ pybabel extract -F babel.cfg -o messages.pot .`

`$ pybabel update -i messages.pot -d translations`

Afterwards some strings might be marked as fuzzy (where it tried to figure out if a translation matched a changed key). If you have fuzzy entries, make sure to check them by hand and remove the fuzzy flag before compiling.

`$ pybabel compile -d translations`


## Init Database

(env)user@Machine:~/Projects/dev$ python shell.py 
>>> from app import db
>>> db.create_all()
>>> exit()
