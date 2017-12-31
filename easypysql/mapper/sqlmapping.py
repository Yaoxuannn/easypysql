# coding: utf-8
from ..sql.types import Field


target = None
CREATE = 'CREATE TABLE IF NOT EXISTS'
UPDATE = 'UPDATE'
INSERT = 'INSERT INTO'
DELETE = 'DELETE FROM'
SELECT = 'SELECT {} FROM'
DROP = 'DROP TABLE'


def get_sql(action, table, obj=None):
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
    elif action == INSERT:
        vals = table.map.copy()
        for k in table.get_field():
            if k.auto_increment and not obj.get(k.field_name):
                vals.remove(k.field_name)
        pre_sql += "(%s) VALUES(" % ", ".join(vals)
        values = str([val for val in obj.values()])[1:-1]
        sql = "{}{})".format(pre_sql, values)
        return sql
    elif action == DROP:
        return pre_sql
    elif action == DELETE:
        return "{} {}".format(pre_sql, _where_construct(obj))


def _where_construct(obj):
    where = 'WHERE {}'
    pattern = "{}={}"
    condition = []
    for k, v in obj.items():
        condition.append(pattern.format(k, _format_value(v)))
    return where.format(" AND ".join(condition))


def _format_value(val):
    if isinstance(val, str):
        return "'{}'".format(val)
    return val


def _get_field(item):
    fields = {}
    for k, v in item.__dict__.items():
        if isinstance(v, Field):
            fields.update({k: v})
    return fields


# FOR CREATE ONLY
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
        sql.append("AUTO_INCREMENT" if target != 'SQLite' else "AUTOINCREMENT")
    if field.default is not None:
        sql.append('DEFAULT %s' % str(field.default))
    sql.append(',')
    return ' '.join(sql)
