#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        users.py

    DESCRIPTION
        processing /users/... request to /api/v... URL

    MODIFIED  (MM/DD/YY)
        Na  08/19/2019

"""
__VERSION__ = "1.0.0.08192019"


# imports
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Post

# configuration

# consts

# functions
@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).pagination(
        page, per_page=current_app.config['NA_BLOG_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    page_prev = None
    if pagination.has_prev:
        page_prev = url_for('api.get_user_posts', id=id, page=page-1)
    page_next = None
    if pagination.has_next:
        page_next = url_for('api.get_user_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': page_prev,
        'next': page_next,
        'count': pagination.total
    })

@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts():
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).pagination(
        page, per_page=current_app.config['NA_BLOG_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    page_prev = None
    if pagination.has_prev:
        page_prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    page_next = None
    if pagination.has_next:
        page_next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': page_prev,
        'next': page_next,
        'count': pagination.total
    })

# classes


# main entry
