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

    def __repr__(self):
        return '<User {}>'.format(self.username)

# main entry
