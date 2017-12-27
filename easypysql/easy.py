# coding: utf-8
"""
This is the core module of this micro framework.
Easy object is the middleware and the controller of the others modules.
"""
from .sql.types import Field
from .sql.query import Query
from .url import parse_url
from .connector import base
from .mapper import sqlmapping


class Easy(object):
    def __init__(self, conn):
        self.connector = conn
        self.send = conn.cursor.execute

    def add(self, obj):
        sql = self._mapping_proxy(sqlmapping.INSERT, obj=obj)
        print(sql)

    def remove(self, obj):
        sql = self._mapping_proxy(sqlmapping.DELETE, obj=obj)
        print(sql)

    def update(self, obj):
        pass

    def query(self, item):
        sql = self._mapping_proxy(sqlmapping.SELECT, table=item)
        # print(sql)
        # self.send(sql)
        return Query(self.connector.cursor.fetchall())

    def _create(self, table):
        sql = self._mapping_proxy(sqlmapping.CREATE, table=table)
        print(sql)
        # self.send(sql)

    @staticmethod
    def _mapping_proxy(action, table=None, obj=None):
        if action in [sqlmapping.CREATE, sqlmapping.SELECT]:
            if table in Table.__subclasses__() \
                    or table.__class__ is Field:
                sql = sqlmapping.getsql(action, table)
                pass
            else:
                raise ValueError("Expected the a Table class or a Field instance, got %s" % table.__class__.__name__)
        elif action in [sqlmapping.INSERT, sqlmapping.DELETE]:
            table = obj.__class__
            sql = sqlmapping.getsql(action, table, obj)
        else:
            sql = ''
        return sql

    def commit(self):
        if self.connector.commit:
            self.connector.commit()

    def rollback(self):
        if self.connector.rollback:
            self.connector.rollback()

    def create(self, *args):
        for item in args:
            self._create(item)

    def create_all(self):
        for table in Table.__subclasses__():
            self.create(table)

    def status(self):
        return self.connector.transaction

    def disconnect(self):
        self.connector.disconnect()
        self.connector = None

    def __str__(self):
        return "<EasyObj target={} database={} status={}>".format(
            self.connector.target, self.connector.database, self.status())

    def __repr__(self):
        return self.__str__()


class TableMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        if name == "Table" or name == "Field":
            return type.__new__(mcs, name, bases, attrs)
        # TODO: ADD CHECK
        # Make connection between Table and Fields
        table_name = attrs['__table_name__']
        for key, attr in attrs.items():
            if attr.__class__.__name__ == "Field":
                attr.table_name = table_name
                attr.field_name = key
        return type.__new__(mcs, name, bases, attrs)


class Table(dict, metaclass=TableMetaClass):
    __table_name__ = ""

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)


def easyconnect(provided_url, **kwargs):
    pre_url = parse_url(provided_url)
    items = vars(pre_url)
    real_target = base.connector_map.get(items.pop('target'))
    items.update(kwargs)
    return Easy(real_target(**items))
