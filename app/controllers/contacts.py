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

from flask import Blueprint, render_template, redirect, request, url_for, flash

from app import tasks
from sqlalchemy.exc import IntegrityError

mod = Blueprint('contacts', __name__, url_prefix='/contacts')


@mod.route('/')
def index():
    contacts = readContactsFromFile()
    return render_template('contacts/index.html', contacts=contacts)

@mod.route('/add')
def add():
    pass

@mod.route('/edit')
def edit():
    pass

@mod.route('/delete')
def delete():
    pass

def readContactsFromFile():
    cfile = '/opt/studio/.baresip/contacts'
    f = open(cfile, 'r')
    contacts = []
    id_count = 0
    for line in f:
        if not line.strip().startswith("#"):
            line2 = line.strip().split('"',1)
            if len(line2) > 1:
                contact = line2[1].strip().split('"', 1)
                contacts.append([id_count, contact[0].strip(), contact[1].strip()])
                id_count += 1
    return contacts
