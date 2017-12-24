# coding: utf-8

from . import BaseConnector, ConnectionException
import pymysql


class MysqlConnector(BaseConnector):
    def __init__(self):
        super(MysqlConnector, self).__init__()



    def connect(self):
        pass


    @property
    def transaction(self):
        pass

    @property
    def database(self):
        pass