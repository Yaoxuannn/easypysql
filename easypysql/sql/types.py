# coding: utf-8
from datetime import datetime


class Field(object):

    __name__ = "Field"

    def __init__(self, sqltype, nullable=True, default=None, auto_increment=False, primary_key=False):
        self.nullable = nullable
        self.default = default
        self.auto_increment = auto_increment
        # If auto_increment is True so the primary key should be True
        self.primary_key = True if auto_increment else primary_key
        if isinstance(sqltype, _SQLType):
            self.sqltype = sqltype
        else:
            raise ValueError("Expected SQLType[Integer|String|Time|Blob], got %s" % sqltype.__class__.__name__)
        self._type = sqltype.python_type
        self.raw_data = None
        self.table_name = None
        self.field_name = None

    @property
    def python_type(self):
        return self._type

    @property
    def raw(self):
        return self.raw_data

    def fill(self, value):
        self.raw_data = value

    def __str__(self):
        return str(self.raw)

    def __repr__(self):
        return str(self.raw)


class _SQLType(object):
    def __init__(self):
        self.python_type = None


class Integer(_SQLType):
    __name__ = 'INTEGER'

    def __init__(self, length=0, real=False):
        super(Integer, self).__init__()
        self.python_type = int
        self.length = length
        if length in range(1, 256):
            self.__name__ = 'TINYINT'
        if real:
            self.python_type = float
            self.__name__ = 'FLOAT'

    # TODO: ADD MORE SUPPORT FOR INTEGER


class String(_SQLType):
    __name__ = 'VARCHAR'

    def __init__(self, length=255):
        super(String, self).__init__()
        self.python_type = str
        self.length = length

    # TODO: ADD MORE SUPPORT FOR STRING


class Time(_SQLType):
    __name__ = 'TIME'

    def __init__(self):
        super(Time, self).__init__()
        self.python_type = datetime

    # TODO: ADD MORE SUPPORT FOR TIME


class Blob(_SQLType):
    __name__ = 'BLOB'

    def __init__(self):
        super(Blob, self).__init__()
        self.python_type = bytes

    # TODO: ADD MORE SUPPORT FOR BLOB
