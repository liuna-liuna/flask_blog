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
    NA_BLOG_FOLLOWERS_PER_PAGE = os.environ.get('NA_BLOG_FOLLOWERS_PER_PAGE') or 50
    NA_BLOG_COMMENTS_PER_PAGE = os.environ.get('NA_BLOG_COMMENTS_PER_PAGE') or 20
    SQLALCHEMY_RECORD_QUERIES = True
    NA_BLOG_SLOW_DB_QUERY_TIME = os.environ.get('NA_BLOG_SLOW_DB_QUERY_TIME') or 0.5

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                             'sqlite:///{}'.format(os.path.join(basedir, 'data-dev.sqlite'))

class TestingConfig(Config):
    TESTING = True
    # to easily test forms submission in HTTP POST request: to disable CSRF token
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                             'sqlite:///{}'.format(os.path.join(basedir, 'data.sqlite'))
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # send email to administrator when error happens
        import logging
        from logging.handlers import SMTPHandler
        credentials, secure = None, None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.NA_BLOG_MAIL_SENDER,
            toaddrs=[cls.NA_BLOG_ADMIN],
            subject='{} Application Error'.format(cls.NA_BLOG_SUBJECT_PREFIX),
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # output logs to stderr, docker logs can process them
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # logging into syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'docker': DockerConfig,
          'unix': UnixConfig,
          'default': DevelopmentConfig
          }

# main entry
