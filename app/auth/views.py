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
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from .forms import LoginForm
from ..models import User

# configuration

# consts

# functions
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

# classes

# main entry
