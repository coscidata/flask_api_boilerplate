# -*- coding: utf-8 -*-

from smart_getenv import getenv

DEBUG = getenv('APP_DEBUG', default=False, type=bool)

LOGGER_NAME = 'app'

# mysql
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 2000
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = getenv(
    'SQLALCHEMY_DATABASE_URI',
    default='mysql+pymysql://root:@localhost:3306/app?charset=utf8mb4')

# secret key
SECRET_KEY = getenv('SECRET_KEY', default='testsecretkey')

# redis cache
# REDIS_URL = getenv('REDIS_URL', default='redis://localhost:6379/0')

try:
    from .local_config import *  # noqa
except ImportError:
    pass
