# coding: utf-8

import pymysql
from .base import *


class MysqlConnector(BaseConnector):
    def __init__(self, username=None, password=None, host=None, port=None, database=None, timeout=10,
                 autocommit=False, **kwargs):
        super(MysqlConnector, self).__init__()
        self._db = database
        self.target = "MySQL"
        self.target_info = ""
        self.attribute = {
            "host": host,
            "port": port,
            "user": username,
            "password": password,
            "database": database,
            "connect_timeout": timeout
        }
        self.attribute.update(kwargs)
        self.connect()
        if autocommit:
            self._conn.autocommit(1)

    def connect(self):
        """
        Establish the connection to the mysql database.
        """
        try:
            self._conn = pymysql.connect(**self.attribute)
        except pymysql.err.OperationalError as e:
            raise ConnectionException(e)
        if self._conn:
            self.cursor = self._conn.cursor()
            self.target_info = "MySQL %s" % self._conn.server_version

    @property
    def transaction(self):
        """
        Seems pymysql doesn't provides with methods which can
        return the status of transaction of mysql server.

        This is a ugly implement version of querying transaction status
        """
        sql = "SELECT trx_id FROM information_schema.INNODB_TRX"
        self.cursor.execute(sql)
        if self.cursor.fetchall():
            return True
        return False

    @property
    def database(self):
        return self.database

    def select_db(self, database):
        self._conn.select_db(database)