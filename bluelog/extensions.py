#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    :author: zhouxiaosong
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_ckeditor import CKEditor

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
moment = Moment()
csrf = CSRFProtect()
ckeditor = CKEditor()
toolbar = DebugToolbarExtension()

@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'