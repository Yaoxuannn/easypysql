# coding: utf-8
import re


class URL(object):
    def __init__(self, target=None, username=None, password=None,
                 host=None, port=None, database=None):
        self.target = target
        self.username = username
        self.password = password
        self.host = host
        if port is not None:
            self.port = int(port)
        else:
            self.port = None
        self.database = database


def parse_url(url):
    pattern = re.compile(r"""
        (?P<target>\w+)://
        (?:
            (?P<username>[^:/]*)
            (?::(?P<password>.*))?
        @)?
        (?:
            (?:(?P<host>[0-9.]+))?
            (?::(?P<port>\d+))?
        )?
        (?:/(?P<database>.*))?
        """, re.X)
    m = pattern.match(url)
    res = m.groupdict()
    return URL(**res)

