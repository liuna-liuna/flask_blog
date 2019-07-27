#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        hello.py

    DESCRIPTION
        test flask

    MODIFIED  (MM/DD/YY)
        Na  07/22/2019

"""
__VERSION__ = "1.0.0.07222019"


# imports
from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'data.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['NA_BLOG_ADMIN'] = os.environ.get('NA_BLOG_ADMIN')
app.config['NA_BLOG_SUBJECT_PREFIX'] = '[NA_BLOG]'
app.config['NA_BLOG_MAIL_SENDER'] = 'NA_BLOG Admin<from.na.blog@gmail.com>'

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# consts

# functions
@app.route('/', methods=['GET', 'POST'])
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
            if app.config['NA_BLOG_ADMIN']:
                send_mail(app.config['NA_BLOG_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = in_name
        return redirect(url_for('.index'))
    else:
        return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
                               known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# for errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# to integrate Python shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# send an email via Gmail SMTP server
def send_mail(to, subject, template, **kwargs):
    msg = Message('{}{}'.format(app.config['NA_BLOG_SUBJECT_PREFIX'], subject),
                  sender=app.config['NA_BLOG_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template('{}.txt'.format(template), **kwargs)
    msg.html = render_template('{}.html'.format(template), **kwargs)
    mail.send(msg)


# classes
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class TODO(object):
    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)


# main entry
if __name__ == "__main__":
    # TODO()()
    app.run()
    #