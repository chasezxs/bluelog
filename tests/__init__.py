#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    :author: zhouxiaosong
"""
from flask import Flask
import logging

app = Flask(__name__)


# @app.route('/')
# def root():
#     app.logger.info('info log')
#     app.logger.warning('warning log')
#     return 'hello'

if __name__ == '__main__':
    app.debug = True
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.logger.warning('warning log')
    app.run()