# -*- coding: utf-8 -*-

from enum import Enum, unique

from flask_sqlalchemy import Pagination
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.inspection import inspect

from app.client import db
from app.const import DEFAULT_COUNT_PRE_PAGE, DEFAULT_PAGE
from app.libs.exception import (InvalidParameter, MissingRequiredField,
                                ObjectNotFound, ProhibitEditField)
from app.libs.jsonutils import Jsonized

CREATED_AT_DEFAULT_VAL = 'CURRENT_TIMESTAMP'
UPDATED_AT_DEFAULT_VAL = 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'


@unique
class Status(Enum):
    DELETED = -1
    OFFLINE = 0
    ONLINE = 1


VALID_STATUS = {s.value for s in Status if s != Status.DELETED}


class BaseModelMixin(Jsonized, db.Model):
    __abstract__ = True

    status = db.Column(db.SmallInteger, default=Status.ONLINE.value)
    created_at = db.Column(
        db.TIMESTAMP(True),
        nullable=False,
        server_default=db.text(CREATED_AT_DEFAULT_VAL))
    updated_at = db.Column(
        db.TIMESTAMP(True),
        nullable=False,
        server_default=db.text(UPDATED_AT_DEFAULT_VAL))

    @property
    def return_fields(self):
        return self.__table__.columns.keys()

    @classmethod
    def required_fields(cls):
        return [
            f for f, v in cls.__table__.columns.items()
            if getattr(v, 'info', {}).get('creatable')
        ]

    @classmethod
    def editable_fields(cls):
        return [
            f for f, v in cls.__dict__.items()
            if getattr(v, 'info', {}).get('editable')
        ]

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.get_id())

    def __eq__(self, other):
        is_same_id = self.get_id() == other.get_id()
        return isinstance(other, self.__class__) and is_same_id

    def to_dict(self):
        return {field: getattr(self, field) for field in self.return_fields}

    def get_id(self):
        """获取主键的值
        """
        return inspect(self).identity[0]

    @staticmethod
    def commit():
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_by_id(cls, id, force=True):
        # because we overrided cls#query
        self = super().query.get(id)
        if self and self.status != Status.DELETED.value:
            return self

        if force:
            raise ObjectNotFound(cls.__name__, id)

        return None

    @hybrid_property
    def query(self):
        return super().query.filter(self.status != Status.DELETED.value)

    @classmethod
    def delete(cls, id):
        self = cls.get_by_id(id)

        self.status = Status.DELETED.value

        if cls.relations:
            for foreign_key in cls.relations:
                foreign_key.class_.delete_by_foreign(foreign_key, id)

        cls.commit()
        return self

    @classmethod
    def delete_by_foreign(cls, foreign_key, id):
        cls.query.filter(
            foreign_key == id).update(dict(status=Status.DELETED.value))

    @classmethod
    def update(cls, id, *args, **kwargs):
        self = cls.get_by_id(id)

        for key in cls.editable_fields():
            val = kwargs.pop(key, None)
            if val:
                setattr(self, key, val)

        if kwargs:
            raise ProhibitEditField(', '.join(kwargs.keys()))

        cls.commit()

        return self

    @classmethod
    def update_status(cls, id, status):
        self = cls.get_by_id(id)

        if status is None or int(status) not in VALID_STATUS:
            raise InvalidParameter('status')

        self.status = status

        cls.commit()

        return self

    @classmethod
    def get_all(cls, page=DEFAULT_PAGE, count=DEFAULT_COUNT_PRE_PAGE):
        if page == 0:
            items = cls.query.all()
            total = len(items)
            return Pagination(None, 1, total, total, items)
        return cls.query.paginate(page, count, False)

    @classmethod
    def create(cls, *args, **kwargs):
        fields = {}
        for field in cls.required_fields():
            val = kwargs.pop(field, None)
            if not val:
                raise MissingRequiredField(field)

            fields[field] = val

        if kwargs:
            raise ProhibitEditField(', '.join(kwargs.keys()))

        model = cls(**fields)
        model.save()

        return model

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e
