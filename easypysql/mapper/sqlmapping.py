# coding: utf-8
from ..sql.types import Field

CREATE = 'CREATE TABLE'
UPDATE = 'UPDATE'
INSERT = 'INSERT INTO'
DELETE = 'DELETE FROM'
SELECT = 'SELECT {} FROM'


def getsql(action, table, obj=None):
    # UPDATE student SET name='Justin' WHERE
    # INSERT INTO student VALUES(XX,XX,XX)
    # DELETE FROM student WHERE
    # SELECT {} FROM student
    if hasattr(table, 'table_name'):
        table_name = table.table_name
    else:
        table_name = table.__table_name__
    pre_sql = "{} {}".format(action, table_name)
    fields = _get_field(table)
    if action == CREATE:
        pre_sql += '('
        sql = []
        for name, field in fields.items():
            sql.append(_parse_field(name, field))
        return "{}{})".format(pre_sql, ''.join(sql)[:-2])
    elif action == SELECT:
        selector = '*'
        if table.__class__ is Field:
            selector = table.field_name
        return pre_sql.format(selector)


def _get_field(item):
    fields = {}
    for k, v in item.__dict__.items():
        if isinstance(v, Field):
            fields.update({k: v})
    return fields


def _operate_field(field):
    pass


# FOR CREATE
def _parse_field(name, field):
    """
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY DEFAULT=5,
    """
    sqltype = field.sqltype
    if field.default is not None and not isinstance(field.default, field.python_type):
        raise ValueError("Expected a %s, got %s" % (field.python_type.__name__, field.default.__class__.__name__))
    # name varchar(255) primary key
    sql = [name, sqltype.__name__ if sqltype.__name__ != 'VARCHAR' else "VARCHAR(%d)" % sqltype.length]
    if not field.nullable:
        sql.append('NOT NULL')
    if field.primary_key:
        sql.append('PRIMARY KEY')
    if field.auto_increment:
        sql.append('AUTO_INCREMENT')
    if field.default is not None:
        sql.append('DEFAULT=%s' % str(field.default))
    sql.append(',')
    return ' '.join(sql)
