#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        authentication.py

    DESCRIPTION
        do authentications for REST API via Flask-HttpAuth

    MODIFIED  (MM/DD/YY)
        Na  08/19/2019

"""
__VERSION__ = "1.0.0.08192019"


# imports
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from . import api
from ..models import User
from .errors import unauthorized, forbidden

# configuration
auth = HTTPBasicAuth()

# consts

# functions
# a callback function
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token is None or email_or_token == '':
        return False
    if password is None or password == '':
        # token
        g.current_user = User.verify_auth_token(email_or_token)
        if g.current_user is not None:
            g.token_used = True
        return g.current_user is not None
    # password
    user = User.query.filter_by(email=email_or_token).first()
    if user is None:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

# overwrite 401 error when credentials are invalid in HttpBasicAuth
@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials.')

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account.')

@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials.')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=600), 'expiration': 600})

# classes


# main entry
