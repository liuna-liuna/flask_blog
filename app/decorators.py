#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        decorators.py

    DESCRIPTION
        decorators used in app

    MODIFIED  (MM/DD/YY)
        Na  08/10/2019

"""
__VERSION__ = "1.0.0.08102019"


# imports
from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

# configuration

# consts

# functions
def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not current_user.can(perm):
                abort(403)
            return f(*args, **kwargs)
        return decorated_func
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

# classes

# main entry
