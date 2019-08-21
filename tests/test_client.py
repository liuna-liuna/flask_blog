#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        test_client.py

    DESCRIPTION
        do testing via Flask built-in test_client

    MODIFIED  (MM/DD/YY)
        Na  08/20/2019

"""
__VERSION__ = "1.0.0.08202019"


# imports
import unittest, re
from app import create_app, db
from app.models import User, Role

# configuration

# consts

# functions

# classes
class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Stranger' in response.get_data(as_text=True))  # get_data() returns by default binary bytes.

    def test_register_and_login(self):
        # register a new user
        response = self.client.post('/auth/register', data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat'
        })
        self.assertEqual(response.status_code, 302) # 302 - redirect

        # use the new user account to login
        response = self.client.post('/auth/login', data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search('Hello,\s+John|john!', response.get_data(as_text=True)))
        self.assertTrue('You have not confirmed your account yet' in response.get_data(as_text=True))

        # send confirmation token
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token), follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have confirmed your account' in response.get_data(as_text=True))

        # logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have been logged out' in response.get_data(as_text=True))


# main entry