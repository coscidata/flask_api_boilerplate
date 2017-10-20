# -*- coding: utf-8 -*-


class CustomError(Exception):
    """自定义错误的基类
    使用
    > raise CustomError('error', 4xx|5xx, payload)
    """
    status_code = 400

    def __init__(self, error, status_code=None, payload=None):
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv


class ObjectNotFound(CustomError):
    status_code = 404

    def __init__(self, obj, id):
        error = '{}: {} not found'.format(obj, id)
        super().__init__(error, self.status_code)


class MissingRequiredField(CustomError):
    def __init__(self, filed):
        error = '{} is missing'.format(filed)
        super().__init__(error)


class InvalidParameter(CustomError):
    def __init__(self, parameter=None):
        error = 'invalid parameter {}'.format(parameter)
        super().__init__(error)


class ProhibitEditField(CustomError):
    def __init__(self, parameter=None):
        error = 'prohibit edit or no {} field'.format(parameter)
        super().__init__(error)
