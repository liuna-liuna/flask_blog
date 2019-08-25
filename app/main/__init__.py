#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        __init__.py

    DESCRIPTION
        definition of blueprint main

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
from flask import Blueprint
from ..models import Permission

# configuration

# consts

# functions

# classes

# main entry
main = Blueprint('main', __name__)

from . import views, errors

# add Permission into app_context => Permission could be used in template.
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
