# -*- coding: utf-8 -*-

import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.app import create_app
from app.client import db
from app.models import *  # noqa

app = create_app()
dsn = app.config['SQLALCHEMY_DATABASE_URI']
if not ('127.0.0.1' in dsn or 'localhost' in dsn):
    print("you are not doing this on your own computer")
    print("线上数据库变更联系sa")
    sys.exit()

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
