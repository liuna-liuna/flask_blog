#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        config.py

    DESCRIPTION
        classes for configuration in hierarchy structure

    MODIFIED  (MM/DD/YY)
        Na  07/28/2019

"""
__VERSION__ = "1.0.0.07282019"


# imports
import os

# configuration

# consts
basedir = os.path.abspath(os.path.dirname(__file__))

# functions

# classes
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or u'hard to guess string for CSRF占位符'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '587')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ('true', 'on', 1, True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    NA_BLOG_ADMIN = os.environ.get('NA_BLOG_ADMIN')
    NA_BLOG_SUBJECT_PREFIX = '[NA_BLOG]'
    NA_BLOG_MAIL_SENDER = 'NA_BLOG Admin<from.na.blog@gmail.com>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NA_BLOG_POSTS_PER_PAGE = os.environ.get('NA_BLOG_POSTS_PER_PAGE') or 20

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                             'sqlite:///{}'.format(os.path.join(basedir, 'data-dev.sqlite'))

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                             'sqlite:///{}'.format(os.path.join(basedir, 'data.sqlite'))

config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig
          }

# main entry
