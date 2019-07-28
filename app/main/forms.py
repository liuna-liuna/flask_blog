#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        forms.py

    DESCRIPTION
        definition of NameForm

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# configuration

# consts

# functions

# classes
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# main entry
