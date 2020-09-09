#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    :author: zhouxiaosong
"""
import os

import sys

basedir = os.path.dirname(os.path.dirname(os.path.basename(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BasicConfig(object):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dec key')
    CKEDITOR_ENABLE_CSRF = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_COMMENT_PER_PAGE = 20
    BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    BLUELOG_EMAIL = '123@139.com'
    BLUELOG_MANAGE_POST_PER_PAGE = 10
    BLUELOG_SLOW_QUERY_THRESHOLD = 1
    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    # BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')


class DevelopmentConfig(BasicConfig):
    DEBUG = False
    WTF_CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yt_xk39b@127.0.0.1:3306/bluelog'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')


class Testing(BasicConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')


class ProductionConfig(BasicConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yt_xk39b@127.0.0.1:3306/bluelogproduct'


config = {
    'development': DevelopmentConfig,
    'testing': Testing,
    'production': ProductionConfig
}
