# coding: utf-8
import datetime


class Field(object):
    __name__ = 'field'

    def __init__(self, sqltype, nullable=True, default=None, auto_increment=False, primary_key=False):
        self._null = nullable
        self.default = default
        self.auto_increment = auto_increment
        self.primary_key = True if auto_increment else primary_key
        if isinstance(sqltype, _SQLType):
            self.sqltype = sqltype
        else:
            raise ValueError("Expected SQLType[Integer|String|Time|Blob], got %s" % sqltype.__class__.__name__)
        self._type = sqltype.python_type
        self.raw_data = None

    @property
    def python_type(self):
        return self._type

    @property
    def raw(self):
        return self.raw_data

    def fill(self, value):
        self.raw_data = value


class _SQLType(object):
    def __init__(self):
        self.python_type = None


class Integer(_SQLType):
    __name__ = 'integer'

    def __init__(self, real=False):
        super(Integer, self).__init__()
        self._type = int
        if real:
            self._type = float

    # TODO: ADD MORE SUPPORT FOR INTEGER

class String(_SQLType):
    __name__ = 'string'

    def __init__(self, length=255):
        super(String, self).__init__()
        self._type = str
        self.length = length

    # TODO: ADD MORE SUPPORT FOR STRING


class Time(_SQLType):
    __name__ = 'time'

    def __init__(self):
        super(Time, self).__init__()
        self._type = datetime

    # TODO: ADD MORE SUPPORT FOR TIME


class Blob(_SQLType):
    __name__ = 'blob'

    def __init__(self):
        super(Blob, self).__init__()
        self._type = bytes

    # TODO: ADD MORE SUPPORT FOR BLOB
