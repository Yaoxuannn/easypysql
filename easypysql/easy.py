# coding: utf-8
"""
This is the core module of this micro framework.
Easy object is the middleware and the controller of the others modules.
"""
from .sql.query import Query
from .url import parse_url
from .connector import base
from .mapper import sqlmapping


class Easy(object):
    def __init__(self, conn):
        self.connector = conn
        self.send = conn.cursor.execute

    def add(self):
        pass

    def remove(self):
        pass

    def update(self):
        pass

    def query(self, table):
        action = sqlmapping.SELECT
        sql = sqlmapping.getsql(action, table)
        # self.send(sql)
        return Query()

    def _create(self, table):
        action = sqlmapping.CREATE
        sql = sqlmapping.getsql(action, table)
        print(sql)
        # self.send(sql)
        pass

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
    def __new__(cls, name, bases, attrs):
        if name == "Table":
            return type.__new__(cls, name, bases, attrs)

        return type.__new__(cls, name, bases, attrs)


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








