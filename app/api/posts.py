#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        posts.py

    DESCRIPTION
        processing /posts/... request for /api/v... URL.

    MODIFIED  (MM/DD/YY)
        Na  08/19/2019

"""
__VERSION__ = "1.0.0.08192019"


# imports
from flask import jsonify, request, current_app, url_for, g
from datetime import datetime
from . import api
from .decorators import permission_required
from .errors import forbidden
from ..models import Post, Permission
from app import db


# configuration

# consts


# functions
@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['NA_BLOG_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json())
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id)}

@api.route('/posts/<int:id>')
def get_post(id):
    json_post = Post.query.get_or_404(id)
    return jsonify(json_post.to_json())

@api.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    json_post = Post.query.get_or_404(id)
    if json_post.author != g.current_user and g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions.')
    json_post.body = request.json.get('body', json_post.body)
    db.session.add(json_post)
    db.session.commit()
    return jsonify(json_post.to_json())

# classes


# main entry
