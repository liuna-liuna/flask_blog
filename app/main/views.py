#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        views.py

    DESCRIPTION
        routing for urls

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
from flask import render_template, redirect, url_for, session, current_app
from datetime import datetime
from .forms import NameForm
from . import main
from .. import db
from ..models import User
from ..email import send_mail

# configuration

# consts

# functions
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        in_name = form.name.data
        user = User.query.filter_by(username=in_name).first()
        if user is None:
            user = User(username=in_name)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['NA_BLOG_ADMIN']:
                send_mail(current_app.config['NA_BLOG_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = in_name
        return redirect(url_for('.index'))
    else:
        return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
                               known=session.get('known', False))

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# classes

# main entry
