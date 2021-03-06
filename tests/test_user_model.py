#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        test_user_model.py

    DESCRIPTION
        testcases for User model

    MODIFIED  (MM/DD/YY)
        Na  07/29/2019

"""
__VERSION__ = "1.0.0.07292019"


# imports
import unittest, time
from datetime import datetime
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

# configuration

# consts

# functions

# classes
class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        self.assertTrue(user.confirm(token))

    def test_invalid_confirmation_token(self):
        user = User(password='cat')
        user2 = User(password='dog')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        token = user.generate_confirmation_token()
        self.assertFalse(user2.confirm(token))

    def test_expired_confirmation_token(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token(expiration=1)
        time.sleep(2)
        self.assertFalse(user.confirm(token))

    # @unittest.skip(reason="[fixed: wrong systax in s.loads(token.encode('utf-8')] line 91: AssertionError: False is not true")
    def test_valid_reset_token(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        token = user.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        db.session.commit()
        self.assertTrue(user.verify_password('dog'))

    def test_invalid_reset_token(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        token = user.generate_reset_token()
        self.assertFalse(user.reset_password(token + 'a', 'horse'))
        self.assertTrue(user.verify_password('cat'))

    def test_valid_change_email_token(self):
        user = User(email='john@example.com', password='cat')
        db.session.add(user)
        db.session.commit()
        token = user.generate_change_email_token('susan@example.com')
        self.assertTrue(user.change_email(token))

    def test_invalid_change_email_token(self):
        user = User(email='john@example.com', password='cat')
        user2 = User(email='susan@example.com', password='dog')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        token = user.generate_change_email_token('david@example.com')
        self.assertFalse(user2.change_email(token))
        self.assertTrue(user2.email == 'susan@example.com')

    def test_duplicate_change_email_token(self):
        user = User(email='john@example.com', password='cat')
        user2 = User(email='susan@example.com', password='dog')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        token = user.generate_change_email_token('john@example.com')
        self.assertFalse(user2.change_email(token))
        self.assertTrue(user2.email == 'susan@example.com')

    def test_user_role(self):
        role = Role.query.filter_by(name='User').first()
        self.assertTrue(role.has_permission(Permission.FOLLOW))
        self.assertTrue(role.has_permission(Permission.WRITE))
        self.assertTrue(role.has_permission(Permission.COMMENT))
        self.assertFalse(role.has_permission(Permission.MODERATE))
        self.assertFalse(role.has_permission(Permission.ADMIN))

    def test_moderator_role(self):
        role = Role.query.filter_by(name='Moderator').first()
        self.assertTrue(role.has_permission(Permission.FOLLOW))
        self.assertTrue(role.has_permission(Permission.WRITE))
        self.assertTrue(role.has_permission(Permission.COMMENT))
        self.assertTrue(role.has_permission(Permission.MODERATE))
        self.assertFalse(role.has_permission(Permission.ADMIN))

    def test_administrator_role(self):
        role = Role.query.filter_by(name='Administrator').first()
        self.assertTrue(role.has_permission(Permission.FOLLOW))
        self.assertTrue(role.has_permission(Permission.WRITE))
        self.assertTrue(role.has_permission(Permission.COMMENT))
        self.assertTrue(role.has_permission(Permission.MODERATE))
        self.assertTrue(role.has_permission(Permission.ADMIN))

    def test_anonymous_role(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.FOLLOW))
        self.assertFalse(user.can(Permission.WRITE))
        self.assertFalse(user.can(Permission.COMMENT))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))

    def test_timestamps(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        self.assertTrue((datetime.utcnow() - user.member_since).total_seconds() < 3)
        self.assertTrue((datetime.utcnow() - user.last_seen).total_seconds() < 3)

    def test_ping(self):
        user = User(password='cat')
        db.session.add(user)
        db.session.commit()
        last_seen_before = user.last_seen
        time.sleep(2)
        user.ping()
        self.assertTrue(user.last_seen > last_seen_before)

    def test_gravatar(self):
        user = User(email='john@example.com', password='cat')
        # with is to fix RuntimeError: Working outside of request context.
        #   gravatar(...) needs an active HTTP request: it calls request.....
        with self.app.test_request_context('/'):
            gravatar = user.gravatar()
            gravatar_256 = user.gravatar(size=256)
            gravatar_pg = user.gravatar(rating='pg')
            gravatar_retro = user.gravatar(default='retro')
        self.assertTrue('https://secure.gravatar.com/avatar/d4c74594d841139328695756648b6bd6' in gravatar \
                        or 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6' in gravatar)
        self.assertTrue('s=256' in gravatar_256)
        self.assertTrue('r=pg' in gravatar_pg)
        self.assertTrue('d=retro' in gravatar_retro)

    # .count()-1 -2 is to minus follow self
    def test_follows(self):
        user1 = User(email='john@example.com', password='cat')
        user2 = User(email='susan@example.com', password='dog')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertFalse(user2.is_following(user1))
        timestamp_before = datetime.utcnow()
        user1.follow(user2)
        db.session.add(user1)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertTrue(user2.is_followed_by(user1))
        self.assertFalse(user2.is_following(user1))
        self.assertFalse(user1.is_followed_by(user2))
        f1 = user1.followed.all()[-1]
        self.assertTrue(f1.followed == user2)
        f2 = user2.followers.all()[-1]
        self.assertTrue(f2.follower == user1)
        self.assertTrue(user1.followed.count()-1 == 1)
        self.assertTrue(user2.followers.count()-1 == 1)
        timestamp_after = datetime.utcnow()
        self.assertTrue(timestamp_before < f1.timestamp < timestamp_after)
        user1.unfollow(user2)
        db.session.add(user1)
        db.session.commit()
        self.assertTrue(user1.followed.count()-1 == 0)
        self.assertTrue(user2.followers.count()-1 == 0)
        self.assertTrue(Follow.query.count()-2 == 0)
        user2.follow(user1)
        db.session.add(user2)
        db.session.add(user1)
        db.session.commit()
        db.session.delete(user2)
        db.session.commit()
        self.assertTrue(Follow.query.count()-1 == 0)

    def test_to_json(self):
        u = User(email='john@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        # RuntimeError: Application was not able to create a URL adapter for request independent URL generation.
        # You might be able to fix this by setting the SERVER_NAME config variable.
        #   to_json(...) needs an active HTTP request: it calls url_for.....
        with self.app.test_request_context('/'):
            json_user = u.to_json()
        expected_keys = ['url', 'username', 'member_since', 'last_seen', 'confirmed',
                         'posts_url', 'followed_posts_url', 'posts_count']
        self.assertEqual(sorted(expected_keys), sorted(json_user.keys()))
        self.assertEqual(json_user.get('url'), '/api/v1/users/{:d}'.format(u.id))

# main entry
