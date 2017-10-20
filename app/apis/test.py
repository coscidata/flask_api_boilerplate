# -*- coding: utf-8 -*-

from flask import abort, request

from app.const import PAGE_COUNT_PARAMS
from app.libs.bputils import create_api_blueprint
from app.libs.decorators import query_params
from app.libs.exception import ObjectNotFound

bp = create_api_blueprint('test', __name__, url_prefix='/test')


@bp.route('/hello', methods=['GET'])
def hello():
    return {'msg': 'hello world!'}


@bp.route('/test', methods=['GET'])
def test():
    abort(400, 'fuck', 'wtf')


@bp.route('/fatal', methods=['GET'])
def fatal():
    how = request.args.get('how')

    if how == '404':
        raise ObjectNotFound('not found')

    raise Exception('😆')


@bp.route('/params/<int:id>', methods=['GET'])
@query_params(**PAGE_COUNT_PARAMS)
def test_params(id, page, count, time):
    return {'id': id, 'page': page, 'count': count, 'time': time}
