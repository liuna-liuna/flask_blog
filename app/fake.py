#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        fake.py

    DESCRIPTION
        to generate virtual users, posts

    MODIFIED  (MM/DD/YY)
        Na  08/12/2019

"""
__VERSION__ = "1.0.0.08122019"


# imports
from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post

# configuration

# consts
N = 100

# functions
def users(count=N):
    fake = Faker()
    i = 0
    while i<count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def posts(count=N):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count-1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()

# classes

# main entry
