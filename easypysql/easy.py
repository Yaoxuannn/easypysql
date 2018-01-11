# coding: utf-8
"""
This is the core module of this micro framework.
"""
from .sql.types import Field
from .sql.query import Query
from .url import parse_url
from .connector import base
from .mapper import sqlmapping

ConnectionException = base.ConnectionException


class Easy(object):
    """
    Easy object is the middleware and the controller of the others modules.
    Almost every operation via Easy object.

    The basic SQL operation is create, create_all, add, remove, update, query.

    You can use easyObj.commit & easyObj.rollback which calls the connector's function(if supports)
    To get the transaction status, just call easyObj.status() which also use the connector's.

    Don't forget to close or disconnect after you use the easyObj, close and disconnect toward to the same
    """
    def __init__(self, conn):
        self.connector = conn
        self.send = conn.cursor.execute
        sqlmapping.target = conn.target

    def add(self, obj):
        sql = self._mapping_proxy(sqlmapping.INSERT, obj=obj)
        self.send(sql)

    def delete(self, obj):
        sql = self._mapping_proxy(sqlmapping.DELETE, obj=obj)
        self.send(sql)

    def update(self, obj):
        pass

    def query(self, item):
        sql = self._mapping_proxy(sqlmapping.SELECT, table=item)
        self.send(sql)
        query = Query(self.connector.cursor.fetchall())
        if item in Table.__subclasses__():
            query.set_table(item, item.map)
        return query

    def drop(self, *tables):
        for t in tables:
            self._drop(t)

    def drop_all(self):
        for table in Table.__subclasses__():
            self.drop(table)

    def _drop(self, table):
        sql = self._mapping_proxy(sqlmapping.DROP, table=table)
        self.send(sql)

    def _create(self, table):
        sql = self._mapping_proxy(sqlmapping.CREATE, table=table)
        self.send(sql)

    def select_db(self, database):
        self.connector.select_db(database)

    @staticmethod
    def _mapping_proxy(action, table=None, obj=None):
        if action in [sqlmapping.CREATE, sqlmapping.SELECT]:
            if table in Table.__subclasses__() \
                    or table.__class__ is Field:
                sql = sqlmapping.get_sql(action, table)
                pass
            else:
                raise ValueError("Expected the a Table class or a Field instance, got %s" % table.__class__.__name__)
        elif action in [sqlmapping.INSERT, sqlmapping.DELETE]:
            table = obj.__class__
            sql = sqlmapping.get_sql(action, table, obj)
        else:
            sql = sqlmapping.get_sql(action, table, obj)
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

    def close(self):
        self.disconnect()

    def __str__(self):
        return "<EasyObj target={} database={} status={}>".format(
            self.connector.target, self.connector.database, self.status())

    def __repr__(self):
        return self.__str__()


class _TableMetaClass(type):
    """
    MetaClass for the Table class
    """
    def __new__(mcs, name, bases, attrs):
        if name == "Table" or name == "Field":
            return type.__new__(mcs, name, bases, attrs)
        # TODO: ADD SOME CHECKS
        attrs.update({"map": []})
        if '__table_name__' not in attrs:
            attrs['__table_name__'] = name.lower()
        # Make connection between Table and Fields
        table_name = attrs['__table_name__']
        for key, attr in attrs.items():
            if attr.__class__.__name__ == "Field":
                attr.table_name = table_name
                attr.field_name = key
                attrs['map'].append(key)
        return type.__new__(mcs, name, bases, attrs)


class Table(dict, metaclass=_TableMetaClass):
    """
    As the table inherit from the native dict Class, it's easy to use.
    """
    __table_name__ = ""

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        for k, v in vars(self.__class__).items():
            if v.__class__.__name__ == "Field":
                if getattr(v, 'default') is not None:
                    self.setdefault(k, getattr(v, 'default'))
                    v.fill(getattr(v, 'default'))
                else:
                    if k not in kwargs and getattr(v, 'auto_increment') is None:
                        raise KeyError('Unspecified key %s with no default attribute' % k)
                if k in kwargs:
                    v.fill(kwargs[k])

    @classmethod
    def get_field(cls):
        fields = []
        for k, v in vars(cls).items():
            if v.__class__.__name__ == "Field":
                fields.append(v)
        return fields


def easyconnect(provided_url, **kwargs):
    """
    The way of getting the instance of Easy
    :param provided_url:
    URL should be like this: PROTO://USER:PASS@HOST/DB, PROTO is required.
    e.g: sqlite:///test  |  mysql://user:pass@localhost/test
    :param kwargs: The params for connection like timeout
    :return: EasyObj
    """
    pre_url = parse_url(provided_url)
    items = vars(pre_url)
    real_target = base.connector_map.get(items.pop('target'))
    items.update(kwargs)
    return Easy(real_target(**items))


connect = easyconnect
