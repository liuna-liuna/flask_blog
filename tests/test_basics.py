#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        test_basics.py

    DESCRIPTION
        basic unit testing

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
import unittest
from flask import current_app
from app import create_app, db

# configuration

# consts

# functions

# classes
class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exits(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


# main entry
