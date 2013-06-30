from flask import Blueprint, render_template

from app import db
from app.models.contacts import Contact

mod = Blueprint('contacts', __name__, url_prefix='/contacts')

@mod.route('/')
def index():
    contacts = Contact.query.all()
    return render_template("contacts/index.html", contacts=contacts)

@mod.route('/add/')
def add():
    contact = Contact('test2', 'fe80::21e:68ff:fed5:333')
    db.session.add(contact)
    db.session.commit()
    return render_template("contacts/add.html")
