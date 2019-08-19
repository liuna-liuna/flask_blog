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
import os, click, sys
from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

# configuration
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

# consts

# functions
# to integrate Python shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
# def test(test_names):
def test(coverage, test_names):
    """Run the unit tests."""
    # set FLASK_COVERAGE env.-variable and restart self
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        # to fix error:
        #   d:\workspace\pweb\scripts\python.exe: can't open file 'd:\workspace\pweb\scripts\flask':
        #                                         [Errno 2] No such file or directory
        #
        sys.argv[0] += '.exe'
        # print('[TO debug] sys.executable={}\nsys.argv={}'.format(sys.executable, sys.argv))
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    # tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    # check coverage
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://{}/index.html'.format(covdir))
        COV.erase()

# classes

# # main entry
# if __name__ == "__main__":
#     app.run()
