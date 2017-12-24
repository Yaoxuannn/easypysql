"""
This is the core module of this micro framework.
Easy object is the middleware and the controller of the others modules.
"""

from .url import parse_url
from .connector import base
from .sqltypes import types


class Easy(object):
    def __init__(self, conn):
        self.connector = conn

    def add(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def query(self):
        pass

    def create(self):
        pass


class Table(object):
    __table_name__ = ""
    pass


def easyconnect(provided_url, **kwargs):
    pre_url = parse_url(provided_url)
    real_target = base.connector_map.get(pre_url.target)
    return real_target(pre_url.database)









