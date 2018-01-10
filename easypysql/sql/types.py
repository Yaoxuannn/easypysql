# coding: utf-8
from datetime import datetime


class _Comparotor(object):
    """
    To support filter function, add this class to handle comparision.
    """
    def __init__(self):
        self.field_name = None
        self.python_type = None

    def __lt__(self, other):
        self._check_type(self, other)
        return self.field_name, "<", other

    def __le__(self, other):
        self._check_type(self, other)
        return self.field_name, "<=", other

    def __ge__(self, other):
        self._check_type(self, other)
        return self.field_name, ">=", other

    def __gt__(self, other):
        self._check_type(self, other)
        return self.field_name, ">", other

    def __eq__(self, other):
        self._check_type(self, other)
        return self.field_name, "=", other

    @staticmethod
    def _check_type(field, other):
        if not isinstance(other, field.python_type):
            raise TypeError("Cannot make comparision between %s and %s" % (field.python_type.__name__, other.__class__.__name__))


class Field(_Comparotor):
    """
    Field object is mapped as the row of the table in database,
    this framework only support limited attributes: null default
    auto_increment primary_key.

    The fill method will set the value of field, but it is strongly not
    recommend you to call this method. It may cause some bad effect.
    """

    __name__ = "Field"

    def __init__(self, sqltype, nullable=True, default=None, auto_increment=False, primary_key=False):
        super(Field, self).__init__()
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
        self._raw_data = None
        self.table_name = None

    @property
    def python_type(self):
        return self._type

    @python_type.setter
    def python_type(self, value):
        self._type = value

    @property
    def raw(self):
        return self._raw_data

    def fill(self, value):
        self._raw_data = value


class _SQLType(object):
    """
    Basic SQLType.
    """
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
