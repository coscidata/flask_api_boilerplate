# -*- coding: utf-8 -*-
import os
from functools import partial

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

from app.config import DEBUG
from app.const import BASE_DIR
from app.libs.exception import CustomError
from app.libs.jsonutils import jsonize

INTERNAL_SERVER_ERROR = 500
ERROR_CODES = [400, 401, 403, 404, 408]
DEFAULT_RETURN_VALUE = {'error': None}


def get_apis_blueprints(exclude=None):
    if not exclude:
        exclude = []

    api_dir = os.path.join(BASE_DIR, 'app/apis')
    return [
        i.split('.')[0] for i in os.listdir(api_dir)
        if not (i.startswith('__') or i in exclude)
    ]


class URLPrefixError(Exception):
    pass


def patch_blueprint_route(bp):
    origin_route = bp.route

    def patched_route(self, rule, **options):
        def decorator(f):
            origin_route(rule, **options)(jsonize(f))

        return decorator

    bp.route = partial(patched_route, bp)


def create_api_blueprint(name, import_name, url_prefix=None, jsonize=True):
    """方便创建 api blueprint 增加 4xx 请求处理，返回值 json 化
    name, import_name, url_prefix 同 Blueprint
    jsonize 等于 Ture 时，自动帮忙序列化，反之没有处理

    在 debug 模式下，500 的错误不进行处理，走 flask 默认的处理，方便调试

    使用：

    from flask import abort

    abort(404, 'xxx not found') or abort(404, 'xxx not found', 'response')
    request 返回 {'error': 'xxx not found', 'msg': 'response'}, 404

    raise Exception('xxx')
    request 返回 {'error': 'xxx'}, 500

    """

    if not url_prefix.startswith('/'):
        raise URLPrefixError(
            'url_prefix ("{}") must start with /'.format(url_prefix))

    bp = Blueprint(name, import_name, url_prefix=url_prefix)

    def _error_hanlder(error):
        # 处理自定义错误
        if issubclass(error.__class__, CustomError):
            return jsonify(error.to_dict()), error.status_code

        # 处理 abort 错误
        if isinstance(error, HTTPException):
            return jsonify({
                'error': error.description,
                'msg': error.response
            }), error.code

        # 处理其他错误
        return jsonify({'error': str(error)}), INTERNAL_SERVER_ERROR

    for code in ERROR_CODES:
        bp.errorhandler(code)(_error_hanlder)

    bp.errorhandler(CustomError)(_error_hanlder)

    if not DEBUG:
        bp.errorhandler(INTERNAL_SERVER_ERROR)(_error_hanlder)

    if jsonize:
        patch_blueprint_route(bp)

    return bp
