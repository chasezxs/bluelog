#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    :author: zhouxiaosong
"""
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, login_required, logout_user

from bluelog.models import Admin
from bluelog.forms import LoginForm
from bluelog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remerber = form.remerber.data
        admin = Admin.query.filter_by(username=username).first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remerber)
                flash('Welcome back', 'info')
                return redirect_back()
            flash('Invaild username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Lout success.', 'info')
    return redirect_back()


