#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        errors.py

    DESCRIPTION
        error handling in REST API

    MODIFIED  (MM/DD/YY)
        Na  08/19/2019

"""
__VERSION__ = "1.0.0.08192019"


# imports
from flask import jsonify
from . import api
from app.exceptions import ValidationError

# configuration

# consts

# functions
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

# classes


# main entry
