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
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# configuration

# consts

# functions

# classes
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