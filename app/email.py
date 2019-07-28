#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        email.py

    DESCRIPTION
        send an email via Gmail SMTP server

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
from flask import render_template, current_app
from threading import Thread
from flask_mail import Message
from . import mail

# configuration

# consts

# functions
def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message('{}{}'.format(app.config['NA_BLOG_SUBJECT_PREFIX'], subject),
                  sender=app.config['NA_BLOG_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template('{}.txt'.format(template), **kwargs)
    msg.html = render_template('{}.html'.format(template), **kwargs)
    t = Thread(target=send_mail_async, args=[app, msg])
    t.start()
    return t

# classes

# main entry
