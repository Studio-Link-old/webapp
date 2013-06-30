from flask import Blueprint, render_template

from app import db
from app.models.contacts import Contact

mod = Blueprint('contacts', __name__, url_prefix='/contacts')

@mod.route('/')
def index():
    return render_template("contacts/index.html")
