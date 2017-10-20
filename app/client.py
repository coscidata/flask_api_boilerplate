# -*- coding: utf-8 -*-

import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, exc
from sqlalchemy.pool import Pool

from app.config import LOGGER_NAME


@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        raise exc.DisconnectionError()
    try:
        cursor.close()
    except AttributeError:
        pass


# mysql
db = SQLAlchemy()

# redis
# rds = Redis.from_url(REDIS_URL)

# logger
logging.basicConfig(
    level=logging.INFO,
    format=  # noqa
    '[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s @ %(lineno)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z')
logger = logging.getLogger(LOGGER_NAME)
