#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        TODO

    DESCRIPTION
        TODO

    MODIFIED  (MM/DD/YY)
        Na  08/19/2019

"""
__VERSION__ = "1.0.0.08192019"


# imports
from flask import g
from functools import wraps
from .errors import forbidden

# configuration

# consts

# functions
def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(perm):
                return forbidden('Insufficient permissions.')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# classes


# main entry
