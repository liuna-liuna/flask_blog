#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        errors.py

    DESCRIPTION
        routing for errors

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
from flask import render_template
from . import main

# configuration

# consts

# functions
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# classes


# main entry
