"""
This is the core module of this micro framework.
Easy object is the middleware and the controller of the others modules.
"""

import url
import connector
from sqltypes import types


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
    pre_url = url.parse_url(provided_url)
    real_target = connector.connector_map.get(pre_url.target)









