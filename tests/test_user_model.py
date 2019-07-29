#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        test_user_model.py

    DESCRIPTION
        testcases for User model

    MODIFIED  (MM/DD/YY)
        Na  07/29/2019

"""
__VERSION__ = "1.0.0.07292019"


# imports
import unittest
from app.models import User

# configuration

# consts

# functions

# classes
class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verify(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password = 'cat')
        u2 = User(password = 'cat')
        self.assertTrue(u.password_hash != u2.password_hash)

# main entry
