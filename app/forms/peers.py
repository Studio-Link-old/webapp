from flask.ext.wtf import Form, TextField, Required, SelectField
from flask.ext.wtf import ValidationError
import socket


def check_ipv6(form, field):
    try:
        socket.inet_pton(socket.AF_INET6, field.data)
        return True
    except socket.error:
        raise ValidationError('Not a valid IPv6 address!')


class AddForm(Form):
    name = TextField('Name', [Required()])
    host = TextField('Host IPv6', [Required(), check_ipv6])


class CallForm(Form):
    codec = SelectField('Codec', choices=[('opus', 'Opus')])
    audio = SelectField('Audio',
                        choices=[('voice', 'Voice'), ('music', 'Music')])
    bitrate = SelectField('Bitrate (kbit/s)', choices=[
        ('192', '192'),
        ('128', '128'),
        ('96', '96'),
        ('64', '64'),
        ('48', '48'),
        ('32', '32'),
        ('24', '24'),
        ('16', '16'),
        ], default='64')
    jitter = SelectField('Jitter', choices=[
        ('300', '300ms'),
        ('250', '250ms'),
        ('200', '200ms'),
        ('150', '150ms'),
        ('100', '100ms'),
        ('50', '50ms'),
        ('25', '25ms'),
        ('10', '10ms'),
        ], default='150')
    framesize = SelectField('Framesize', choices=[
        ('60', '60ms'),
        ('40', '40ms'),
        ('20', '20ms'),
        ('10', '10ms'),
        ('5', '5ms'),
        ('2', '2ms'),
        ], default='20')
