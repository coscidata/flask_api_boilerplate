# -*- coding: utf-8 -*-

import logging

from flask import Flask
from werkzeug.utils import import_string

from app.client import db, logger
from app.config import DEBUG
from app.libs.bputils import get_apis_blueprints

HEADERS = {
    'Access-Control-Max-Age': '1728000',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, HEAD',
}


def create_app():
    """create app function return flask app instance"""
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.secret_key = app.config['SECRET_KEY']

    app.url_map.strict_slashes = False

    db.init_app(app)

    if DEBUG:
        logger.setLevel(logging.DEBUG)

    for bp_name in get_apis_blueprints():
        import_name = '%s.apis.%s:bp' % (__package__, bp_name)
        app.register_blueprint(import_string(import_name))

    @app.after_request
    def after_request(resp):
        for k, v in HEADERS.items():
            resp.headers[k] = v

        return resp

    return app
