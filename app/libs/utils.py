# -*- coding: utf-8 -*-

from functools import wraps

from flask import request


def params_parse(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = {}
        for key in request.args:
            data[key] = request.args.get(key)

        if data:
            kwargs.update(data)
        return f(*args, **kwargs)

    return wrapper
