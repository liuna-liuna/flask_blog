#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        test_selenium.py

    DESCRIPTION
        do testing using selenium as web browser automation

    MODIFIED  (MM/DD/YY)
        Na  08/21/2019

"""
__VERSION__ = "1.0.0.08212019"


# imports
import unittest, threading, re, time
from selenium import webdriver
from app import create_app, db, fake
from app.models import Role, User

# configuration

# consts

# functions

# classes
class SeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create chrome
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome(chrome_options=options)
        except:
            pass

        # do testing only when a browser is started
        if cls.client:
            # create application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # disable logging to keep it clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            # create db and faker data
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # add an administrator
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         confirmed=True, role=admin_role)
            db.session.add(admin)
            db.session.commit()

            # start Flask web server in a thread
            cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'debug': False})
            cls.server_thread.start()

            # give the server a second to ensure it is up
            time.sleep(1)


    @classmethod
    def tearDownClass(cls):
        # close browser and Flask web server
        cls.client.get('http://localhost:5000/shutdown')
        cls.client.quit()
        cls.server_thread.join()

        # destroy db
        db.drop_all()
        db.session.remove()

        # remove app_context
        cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available.')

    def tearDown(self):
        pass

    # @unittest.skip(reason='[1 extra space in index.html: Hello, john !] self.client.page_source is None after login')
    def test_admin_home_page(self):
        # enter app home page
        self.client.get('http://localhost:5000')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

        # enter login page
        self.client.find_element_by_link_text('Log In').click()
        self.assertIn('<h1>Login</h1>', self.client.page_source)

        # login
        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        # print('[DEBUG only] self.client={}\nself.client.page_source:\n'.format(self.client, self.client.page_source))
        self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))

        # enter user profile page
        self.client.find_element_by_link_text('Profile').click()
        self.assertIn('<h1>john</h1>', self.client.page_source)

# main entry
