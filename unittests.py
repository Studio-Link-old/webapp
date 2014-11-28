#!/usr/bin/env python
# +--------------------------------------------------------------------------+
# |   _____ __            ___          __    _       __                      |
# |  / ___// /___  ______/ (_)___     / /   (_)___  / /__                    |
# |  \__ \/ __/ / / / __  / / __ \   / /   / / __ \/ //_/                    |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ / / / / ,<                       |
# |/____/\__/\__,_/\__,_/_/\____/  /_____/_/_/ /_/_/|_|                      |
# |Copyright Sebastian Reimers 2013 - 2014 studio-link.de                    |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

import os
from app import app
from app import db
from app.models.accounts import Accounts
import unittest
import tempfile
import redis
from mock import Mock, patch

class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.store = redis.Redis('127.0.0.1')
        self.store.flushall()

    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
                                                self.db_filename
        app.config['TESTING'] = True
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)

    def add_account(self):
        rv = self.client.post('/accounts/add/', data=dict(
            name='Test1',
            server='127.0.0.1',
            username='test',
            password='secret'
            ))
        return rv

##############################################################
# app Tests
##############################################################
    def test_app_empty_db(self):
        """Start with a blank database."""
        rv = self.client.get('/accounts/')
        assert b'Edit' not in rv.data

    def test_app_index(self):
        rv = self.client.get('/')
        assert b'load' in rv.data

    def test_app_404_not_found(self):
        rv = self.client.get('/bigbangtheory')
        assert b'Ups, site not found!' in rv.data

##############################################################
# app.controllers.calls Tests
##############################################################
    @patch('app.libs.baresip.requests')
    def test_calls(self,requests):
        requests.get.return_value = Mock(content = 'Local IPv6:   enp4s11 - fe80::21e:68ff:fed5:9d85')
        rv = self.client.get('/calls/')
        assert b'Dial' in rv.data
    
    @patch('app.libs.baresip.requests')
    def test_calls_dial(self,requests):
        self.add_account()
        requests.get.return_value = Mock(content = 'studio@lan')
        rv = self.client.post('/calls/',data=dict(
            accounts='studio@lan',
            number='studio@fe80::21e:68ff:fed5:9d85',
            ))
        assert b'redirected' in rv.data


##############################################################
# app.controllers.accounts Tests
##############################################################
    def test_accounts_add(self):
        self.add_account()
        rv = self.client.get('/accounts/')
        assert b'Test1' in rv.data

    def test_accounts_edit(self):
        self.add_account()
        rv = self.client.get('/accounts/edit/1')
        assert b'Add/Edit SIP Account' in rv.data

        self.client.post('/accounts/edit/1', data=dict(
            name='Test2',
            server='127.0.0.1',
            username='test',
            password='',
            codecs=['opus']
            ))
        account = Accounts.query.get(1)
        password_old = account.password
        assert 'opus' in account.options
        assert 'gsm' not in account.options

        self.client.post('/accounts/edit/1', data=dict(
            name='Test2',
            server='127.0.0.1',
            username='test',
            password='test1234',
            codecs=['opus','gsm']
            ))
        account = Accounts.query.get(1)
        password_new = account.password
        assert 'opus' in account.options
        assert 'gsm' in account.options
        assert password_new != password_old

        rv = self.client.get('/accounts/')
        assert b'Test1' not in rv.data
        assert b'Test2' in rv.data

    def test_accounts_delete(self):
        self.add_account()
        self.client.get('/accounts/delete/1')
        rv = self.client.get('/accounts/')
        assert b'Test1' not in rv.data

##############################################################
# app.controllers.mixers Tests
##############################################################

    def test_mixers(self):
        rv = self.client.get('/mixers/')
        assert b'Mixer' in rv.data

##############################################################
# app.controllers.settings Tests
##############################################################

    def test_settings(self):
        rv = self.client.get('/settings/')
        assert b'Device' in rv.data

    def test_settings_save(self):
        rv = self.client.post('/settings/', data=dict(password="studio"))
        assert b'Settings' in rv.data
        rv = self.client.post('/settings/', data=dict(password=""))
        assert b'Settings' in rv.data

##############################################################
# app.controllers.system Tests
##############################################################

    def test_system_raw(self):
        rv = self.client.get('/system/raw')
        assert b'cpuusage' in rv.data

    @patch('app.controllers.system.subprocess')
    def test_system_log(self, subprocess):
        rv = self.client.get('/system/log')
        assert b'Log' in rv.data
    
    @patch('app.controllers.system.subprocess')
    def test_system_log_match(self, subprocess):
        rv = self.client.get('/system/log/baresip')
        assert b'Log' in rv.data

    def test_reboot_required(self):
        self.store.set('reboot_required', 'true')
        rv = self.client.get('/')
        assert b'Reboot required' in rv.data
    
    def test_reboot_required_false(self):
        self.store.set('reboot_required', 'false')
        rv = self.client.get('/')
        assert b'Reboot required' not in rv.data

if __name__ == '__main__':
    unittest.main()
