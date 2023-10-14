# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declared_attr
from app.ext.utils import Commons
import logging as log


class GenericModel(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def save(cls, _data=None):
        try:
            if _data is None:
                db.session.add(cls)
            else:
                db.session.add(_data)

            resp = db.session.commit()
            return resp
        except Exception as e:
            db.session.rollback()
            log.warning("save Exception: {0}".format(e))
            return e

    @classmethod
    def update(cls, _data=None):
        try:
            db.session.add(_data)

            resp = db.session.commit()
            return resp
        except Exception as e:
            db.session.rollback()
            log.warning("update Exception: {0}".format(e.message))
            return e.message

    @classmethod
    def delete(cls, _data=None):
        try:
            db.session.delete(_data)

            resp = db.session.commit()
            return resp
        except Exception as e:
            db.session.rollback()
            log.warning("delete Exception: {0}".format(e.message))
            return e.message

    @classmethod
    def get_all(cls, _limit=0):
        try:
            resp = None
            if _limit == 0:
                resp = db.session.query(cls).all()
            elif _limit > 0:
                resp = db.session.query(cls).limit(_limit).all()

            if resp is None:
                return None
            else:
                return resp
        except Exception as e:
            db.session.rollback()
            log.warning("get_all Exception: {0}".format(e))
            return e

    @classmethod
    def get_by_id(cls, _id=0):
        if _id > 0:
            try:
                resp = cls.query.get(_id)
                if resp is None:
                    return None
                else:
                    return resp
            except Exception as e:
                db.session.rollback()
                log.warning("get_all Exception: {0}".format(e.message))
                return e.message
        else:
            return None

    @classmethod
    def get_by(cls, _name=None, _value=None, result_fetch='one'):
        if _name is None:
            return None

        if _value is None:
            return None

        try:
            resp = None

            if result_fetch is 'one':
                resp = cls.query.filter(getattr(cls, _name) == _value).first()
            elif result_fetch is 'all':
                resp = cls.query.filter(getattr(cls, _name) == _value).all()

            if resp is None:
                return None
            else:
                return resp
        except Exception as e:
            db.session.rollback()
            log.warning("get_by Exception: {0}".format(e.message))
            return e.message

    @classmethod
    def select_from_view(cls, _view=None, _conds=None, result_fetch='one'):
        sql = None

        if _view is None:
            return None

        if _conds is None:
            sql = db.text("SELECT * FROM {0}".format(_view))
        else:
            sql = db.text("SELECT * FROM {0} WHERE {1}".format(_view, _conds))

        try:
            result_query = db.session.execute(sql)
            db.session.commit()

            fetch_query = None

            if result_fetch is 'one':
                fetch_query = result_query.first()
                result_one = dict(fetch_query)
                # return result_one
                return cls.dict_to_obj(result_one)
            # check
            elif result_fetch is 'all':
                fetch_query = result_query.fetchall()
                result_all = cls.raw_json(fetch_query)
                return result_all
        except Exception as e:
            db.session.rollback()
            log.warning("select_from_view Exception: {0}".format(e.message))
            return None

    @classmethod
    def dict_to_obj(cls, _dict=None, _name='from_dict'):
        if _dict is None:
            return None

        try:
            new_obj = type(_name, (object,), _dict)
            return new_obj
        except Exception as e:
            log.warning("dict_to_obj Exception: {0}".format(e.message))
            return None

    @classmethod
    def to_json(cls, obj=None):
        if obj is None:
            return None

        if (Commons.is_iterable(obj)):
            try:
                item_list = []
                num_obj = len(obj)
                if num_obj > 0:
                    for item in obj:
                        new_item = {c.key: unicode(getattr(item, c.key)) for c in inspect(item).mapper.column_attrs}
                        item_list.append(new_item)
                    return item_list
            except Exception as e:
                log.warning("to_json iterable Exception: {0}".format(e.message))
                return e.message

        elif isinstance(obj, cls):
            try:
                resp = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
                return resp
            except Exception as e:
                log.warning("to_json isinstance Exception: {0}".format(e.message))
                return e.message

    @classmethod
    def raw_json(cls, obj=None, default='dict'):
        if obj is None:
            return None

        if default is 'dict':
            try:
                dict_list = []

                for item in obj:
                    dict_list.append(dict(item))

                return dict_list
            except Exception as e:
                log.warning("raw_json dict Exception: {0}".format(e.message))
                return e.message

        elif default is 'tuple':
            try:
                dict_list = []

                for item in obj:
                    # dict_list.append(item._asdict())
                    dict_list.append(Commons.to_json(item._asdict()))

                return dict_list
            except Exception as e:
                log.warning("raw_json _asdict Exception: {0}".format(e.message))
                return e.message

    @classmethod
    def raw_query(cls, _query=None):
        if _query is None:
            return None

        try:
            sql = db.text(_query)
            result = db.session.execute(sql)
            db.session.commit()

            result_fetch = result.fetchall()
            if result_fetch is None:
                return None
            else:
                result_all = cls.raw_json(result_fetch)
                return result_all
        except Exception as e:
            db.session.rollback()
            log.warning("raw_query Exception: {0}".format(e.message))
            return e.message
