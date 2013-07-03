from flask.ext.wtf import Form, TextField, Required

class AddForm(Form):
    name = TextField('Name', [Required()])
    host = TextField('Host IPv6', [Required()])
