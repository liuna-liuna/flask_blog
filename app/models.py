#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        models.py

    DESCRIPTION
        definitions of db via ORM framework SQLAlchemy

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


# configuration

# consts

# functions

# classes
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
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

# main entry
