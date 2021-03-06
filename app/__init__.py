#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        __init__.py

    DESCRIPTION
        initiate app via create_app

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config
from flask_pagedown import PageDown

# configuration

# consts
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
pagedown = PageDown()

# functions
def create_app(config_name):
    # create app
    app = Flask(__name__)
    # print('[TO BE REMOVED] __name__ = {}\nconfig_name = {}\napp = {}'.format(__name__, config_name, app))
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize extension
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # add routing
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

# classes


# main entry
