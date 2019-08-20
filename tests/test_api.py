#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        test_api.py

    DESCRIPTION
        testing REST API

    MODIFIED  (MM/DD/YY)
        Na  08/20/2019

"""
__VERSION__ = "1.0.0.08202019"


# imports
import unittest, json, re
from base64 import b64encode
from flask import url_for
from app import create_app, db
from app.models import User, Role, Post, Comment

# configuration

# consts

# functions

# classes
class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()    # API don't use use_cookies=True

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic {}'.format(
                b64encode(':'.join([username, password]).encode('utf-8')).decode('utf-8')),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def add_a_user_to_db(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

    def test_404(self):
        response = self.client.get('/wrong/url', headers=self.get_api_headers('nouser', 'nopasswd'))
        self.assertEqual(response.status_code, 404)
        # for /wrong/url, response.get_data(as_text=True) has <title><script> etc., but
        #   json.loads(response.get_data(as_text=True)) errors out:
        #       raise JSONDecodeError("Expecting value", s, err.value) from None
        #       json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
        # => use response.status instead, which is '404 NOT FOUND'.
        self.assertEqual(response.status, '404 NOT FOUND')

    def test_no_auth(self):
        # url_for('api.get_posts') didn't work here
        #   RuntimeError: Application was not able to create a URL adapter for request independent URL generation.
        #   You might be able to fix this by setting the SERVER_NAME config variable.
        # <=> with self.app.test_request_context('/'): fixed it.
        with self.app.test_request_context('/'):
            response = self.client.get(url_for('api.get_posts'), content_type='application/json')
        # .get('/api/v1/posts/'...) works too.
        # response = self.client.get('/api/v1/posts/', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_bad_auth(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        response = self.client.get('/api/v1/posts/', headers=self.get_api_headers('john@example.com', 'dog'))
        self.assertEqual(response.status_code, 401)

    def test_token_auth(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # issue a request with a bad token
        response = self.client.get('/api/v1/posts/', headers=self.get_api_headers('notoken', ''))
        self.assertEqual(response.status_code, 401) # 401 Unauthorized due to @auth.verify_password failed

        # get a token
        response = self.client.post('/api/v1/tokens/', headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        token = json_response.get('token')
        self.assertIsNotNone(token)

        # issue a request with the good token
        response = self.client.get('/api/v1/posts/', headers=self.get_api_headers(token, ''))
        self.assertEqual(response.status_code, 200)

    def test_anonymous(self):
        response = self.client.get('/api/v1/posts/', headers=self.get_api_headers('', ''))
        self.assertEqual(response.status_code, 401)

    def test_unconfirmed_account(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=False, role=r)
        db.session.add(u)
        db.session.commit()

        response = self.client.get('/api/v1/posts/', headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 403)

    def test_posts(self):
        # add a new user
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # write an empty post
        response = self.client.post('/api/v1/posts/', headers=self.get_api_headers('john@example.com', 'cat'),
                                    data=json.dumps({'body': ''}))
        self.assertEqual(response.status_code, 400)

        # write a post
        response = self.client.post('/api/v1/posts/', headers=self.get_api_headers('john@example.com', 'cat'),
                                    data=json.dumps({'body': 'body of the *blog* post from test_api'}))
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # retrieve post written just now
        response = self.client.get(url, headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        url_in_response = 'http://localhost{}'.format(json_response['url'])
        self.assertEqual(url_in_response, url)
        self.assertEqual(json_response['body'], 'body of the *blog* post from test_api')
        self.assertEqual(json_response['body_html'], '<p>body of the <em>blog</em> post from test_api</p>')
        json_post = json_response

        # get the post from the user
        response = self.client.get('/api/v1/users/{:d}/posts/'.format(u.id),
                                   headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('posts'))
        self.assertEqual(json_response.get('count', 0), 1)
        self.assertEqual(json_response['posts'][0], json_post)

        # get the post from the user as a follower
        response = self.client.get('/api/v1/users/{:d}/timeline/'.format(u.id),
                                   headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('posts'))
        self.assertEqual(json_response.get('count', 0), 1)
        self.assertEqual(json_response['posts'][0], json_post)

        # edit post
        response = self.client.put(url, headers=self.get_api_headers('john@example.com', 'cat'),
                                   data=json.dumps({'body': 'update post'}))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual('http://localhost{}'.format(json_response.get('url')), url)
        self.assertEqual(json_response.get('body'), 'update post')
        self.assertEqual(json_response.get('body_html'), '<p>update post</p>')

    def test_users(self):
        # add two users
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u1 = User(email='john@example.com', username='john', password='cat', confirmed=True, role=r)
        u2 = User(email='susan@example.com', username='susan', password='dog', confirmed=True, role=r)
        db.session.add_all([u1, u2])
        db.session.commit()

        # get users
        response = self.client.get('/api/v1/users/{:d}'.format(u1.id),
                                   headers=self.get_api_headers('susan@example.com', 'dog'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response.get('username'), 'john')

        response = self.client.get('/api/v1/users/{:d}'.format(u2.id),
                                   headers=self.get_api_headers('susan@example.com', 'dog'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response.get('username'), 'susan')


    def test_comments(self):
        # add two users
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u1 = User(email='john@example.com', username='john', password='cat', confirmed=True, role=r)
        u2 = User(email='susan@example.com', username='susan', password='dog', confirmed=True, role=r)
        db.session.add_all([u1, u2])
        db.session.commit()

        # add a post
        post = Post(body='body of the post', author=u1)
        db.session.add(post)
        db.session.commit()

        # write a comment
        response = self.client.post('/api/v1/posts/{:d}/comments/'.format(post.id),
                                headers=self.get_api_headers('susan@example.com', 'dog'),
                                data=json.dumps({'body': 'Good [post](http://example.com)!'}))
        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.get_data(as_text=True))
        url = response.headers.get('Location')
        self.assertIsNotNone(url)
        self.assertEqual(json_response.get('body'), 'Good [post](http://example.com)!')
        self.assertEqual(re.sub('<.*?>', '', json_response.get('body_html')), 'Good post!')

        # get the comment
        response = self.client.get(url,
                                headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone('http://localhost{}'.format(json_response.get('url')), url)
        self.assertEqual(json_response.get('body'), 'Good [post](http://example.com)!')

        # write another comment
        comment = Comment(body='Thank you!', author=u1, post=post)
        db.session.add(comment)
        db.session.commit()

        # get the two comments from the post
        response = self.client.get('/api/v1/posts/{:d}/comments/'.format(post.id),
                                headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('comments'))
        self.assertEqual(json_response.get('count'), 2)

        # get the two comments from the comments
        response = self.client.get('/api/v1/comments/',
                                headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('comments'))
        self.assertEqual(json_response.get('count'), 2)

# main entry
