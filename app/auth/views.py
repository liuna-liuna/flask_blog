#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        views.py

    DESCRIPTION
        routing for authentication

    MODIFIED  (MM/DD/YY)
        Na  07/29/2019

"""
__VERSION__ = "1.0.0.07292019"


# imports
from flask import render_template
from . import auth

# configuration

# consts

# functions
@auth.route('/login')
def login():
    return render_template('auth/login.html')

# classes

# main entry
