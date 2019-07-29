#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        __init__.py

    DESCRIPTION
        blueprint for authentication

    MODIFIED  (MM/DD/YY)
        Na  07/29/2019

"""
__VERSION__ = "1.0.0.07292019"


# imports
from flask import Blueprint

# configuration

# consts

# functions

# classes

# main entry
auth = Blueprint('auth', __name__)

from . import views