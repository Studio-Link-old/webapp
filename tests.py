#!/usr/bin/env python
import os
from app import app
from app import db
import unittest
import tempfile


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp() 
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.db_filename
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)

    def add_peer(self):
        self.client.post('/peers/add/', data=dict(
            name='Test1',
            host='::'
            ))

    def test_empty_db(self):
        """Start with a blank database."""
        rv = self.client.get('/peers/')
        assert b'No entries here so far' in rv.data

    def test_add_peer(self):
        self.add_peer()
        rv = self.client.get('/peers/')
        assert b'Test1' in rv.data

if __name__ == '__main__':
    unittest.main()
