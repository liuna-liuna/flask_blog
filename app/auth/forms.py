#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        forms.py

    DESCRIPTION
        definition of LoginForm

    MODIFIED  (MM/DD/YY)
        Na  07/29/2019

"""
__VERSION__ = "1.0.0.07292019"


# imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

# configuration

# consts

# functions

# classes
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# main entry
