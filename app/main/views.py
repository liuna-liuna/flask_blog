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
from flask import render_template, redirect, url_for, session, current_app, flash
from flask_login import current_user, login_required
from datetime import datetime
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from . import main
from .. import db
from ..models import User, Role
from ..email import send_mail
from ..decorators import admin_required

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

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.email.username
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile of {} has been updated.'.format(user.username))
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


# classes

# main entry
