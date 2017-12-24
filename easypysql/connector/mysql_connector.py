# coding: utf-8

import pymysql
from .base import *


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