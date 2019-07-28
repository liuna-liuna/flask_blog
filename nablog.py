#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        nablog.py

    DESCRIPTION
        main entry for flask blog system nablog

    MODIFIED  (MM/DD/YY)
        Na  07/22/2019

"""
__VERSION__ = "1.0.0.07222019"


# imports
from flask_migrate import Migrate
import os, click
from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

# configuration

# consts

# functions
# to integrate Python shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# classes

# main entry
if __name__ == "__main__":
    app.run()
