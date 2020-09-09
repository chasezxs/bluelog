#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    :author: zhouxiaosong
"""
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries

from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.extensions import db, migrate, bootstrap, login_manager, moment, csrf, ckeditor, toolbar
from bluelog.models import Admin, Category, Link, Comment
from bluelog.settings import config

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_logging(app)
    register_request_handlers(app)
    register_extensions(app)
    register_commands(app)
    register_blueprints(app)
    register_template_context(app)
    return app


def register_logging(app):
    # class RequestFromatter(logging.Formatter):
    #     def format(self, record):
    #         record.url = request.url
    #         record.remote_addr = request.remote_addr
    #         return super(RequestFromatter, self).format(record)
    #
    # request_formater = RequestFromatter(
    #     '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    #     '%(levelname)s in %(module)s: %(message)s'
    # )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # mail_handler = SMTPHandler(
    #     mailhost=app.config['MAIL_SERVER'],
    #     fromaddr=app.config['MAIL_USERNAME'],
    #     toaddrs=['ADMIN_EMAIL'],
    #     subject='Bluelog Application Error',
    #     credentials=(app.config['MAIL_USERNAME', app.config['MAIL_PASSWORD']])
    # )
    # mail_handler.setLevel(logging.ERROR)
    # mail_handler.setFormatter(request_formater)

    if not app.debug:
        # app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    toolbar.init_app(app)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login')
    def init(username, password):
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administator account...')
            admin = Admin(
                username=username,
                blog_title='Bluelog',
                blog_sub_title="No, I'm the real thing.",
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')

    @app.cli.command('select')
    def select_post():
        from bluelog.fakes import select_posts
        select_posts()


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, links=links, unread_comments=unread_comments)


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n' % (q.duration, q.context, q.statment)
                )
        return response
