import datetime


class Field(object):
    __name__ = 'field'

    def __init__(self, sqltype, nullable=True, default=None, auto_increment=False, primary_key=False):
        self._null = nullable
        self.default = default
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        if isinstance(sqltype, SQLType):
            self.sqltype = sqltype
        else:
            raise ValueError("Expected SQLType[Integer|String|Time|Blob], got %s" % sqltype.__class__.__name__)
        self._type = sqltype.python_type
        self.raw_data = None

    @property
    def python_type(self):
        return self._type

    def fill(self, value):
        self.raw_data = value


class SQLType(object):
    def __init__(self):
        self.python_type = None


class Integer(SQLType):
    __name__ = 'integer'

    def __init__(self, real=False):
        super(Integer, self).__init__()
        self._type = int
        if real:
            self._type = float


class String(SQLType):
    __name__ = 'string'

    def __init__(self, length):
        super(String, self).__init__()
        self._type = str
        self.length = length


class Time(SQLType):
    __name__ = 'time'

    def __init__(self):
        super(Time, self).__init__()
        self._type = datetime


class Blob(SQLType):
    __name__ = 'blob'

    def __init__(self):
        super(Blob, self).__init__()
        self._type = bytes
