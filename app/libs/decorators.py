# -*- coding: utf-8 -*-

import functools
import inspect

from flask import request

from app.libs.exception import InvalidParameter, MissingRequiredField


def query_params(**config):
    """处理、校验 request 参数，并且当做参数传入 api 函数中

    使用:
    1:  所有参数配置 config
        @bp.route(xxx)
        @query_params(page={'default': default, 'type_': int, 'required': True, 'min_': 0, 'max_': 999})
        def test(page, count):
            xxx

    2:
        参数不带config，默认值为 None
        @bp.route(xxx)
        @query_params(page={'default': default, 'type_': int, 'required': True, 'min_': 0, 'max_': 999})
        def test(page, count, time):
            xxx

    参数:
    default: 默认值(可选)
    type_: 参数类型(可选)
    required: 是否必须，默认为 False (可选)
    min_: 最小值, 如果是字符类型，为长度 (可选)
    max_: 最大值, 如果是字符类型，为长度 (可选)

    异常：
    * 值缺失抛 MissingRequiredField
    * 值校验失败抛 InvalidParameter

    使用 is None 防止 0 值
    """

    def __query_params(func):
        need_params = inspect.getfullargspec(func).args

        @functools.wraps(func)
        def __(*args, **kwargs):
            request_params = request.values

            # 最后返回的参数列表
            params = {}

            for param in need_params:
                val = request_params.get(param) or kwargs.get(param)

                conditions = config.get(param)

                # 如果没有 config，不做任何处理，默认值就是 None
                if not conditions:
                    params[param] = val
                    continue

                # 检查是否必须
                required = conditions.get('required', False)
                if required and val is None:
                    raise MissingRequiredField(param)

                # 检查是否有默认值
                default = conditions.get('default')
                if default is not None and val is None:
                    params[param] = default
                    continue

                # 检查类型是否正确，避免使用 type 关键字
                type_ = conditions.get('type_')
                if type_:
                    try:
                        val = type_(val)
                    except ValueError:
                        raise InvalidParameter(param)

                # 检查范围，如果字符类型比较长度，否则比较数值本身
                min_ = conditions.get('min_')
                max_ = conditions.get('max_')
                v = val
                if isinstance(val, str) or isinstance(val, bytes):
                    v = len(val)

                if (min_ and v < min_) or (max_ and v > max_):
                    raise InvalidParameter(param)

                params[param] = val

            return func(**params)

        return __

    return __query_params
