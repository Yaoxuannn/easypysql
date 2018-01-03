# Easypysql

This is a small and simple ORM micro-framework implements with Python3. Here is a simple introduction of it and the instruction for using. (**PLEASE DO NOT USE IT IN A PRODUCTION ENV.**)

## Introduction

Following is the structure of the whole framework.

```
easypysql
├── __init__.py
├── connector
│   ├── __init__.py
│   ├── base.py
│   ├── mysql_connector.py
│   └── sqlite_connector.py
├── easy.py
├── mapper
│   ├── __init__.py
│   └── sqlmapping.py
├── sql
│   ├── __init__.py
│   ├── query.py
│   └── types.py
└── url.py
```

The core module of this framework is `easy.py` which performs as the interactor for users. And it is the entry of this ORM framework.

As you see the connector package is the driver for `Easypysql`. It is **possible** to support more types of databases as the  new `DB_connector` inherits the `BaseConnector` and implements in a proper way, just like the plugin.

Almost every Object-SQL transform are done in the `mapper.sqlmapping`.

The url module is more like a util module, I write this module (And i learnt some regular expression from SQLalchemy.) to support URL-connect method, and modified the component which i will show you in the next part of this article.

## Instruction

I name this ORM cake **`easypysql`**, that means it is easy to use. Additionally, only use it in a easy condition.

### Get it easy

As you learnt in the introduction part, the core module is `easy.Easy`. So, how to get it?

```python
from easypysql.easy import easyconnect, ConnectionException

path = '/tmp/tmpdb'

try:
    easy = easyconnect("sqlite:///%s" % path, timeout=10)
except ConnectionException:
    pass
```

the method `easyconnect` has an alias as `connect`, which has the exactly same effect of the former. This action is for someone who don't like the name of `easyconnect`. As this method called, a connection will be established.

> The standard of url is : `PROTO://USER:PASS@HOST:PORT/DATABASE`

Now you can use `easy` to do some cool things!

**Remember: When you finish the easy using, please close or disconnect it.** Like the following code shows:

```python
easy.close()
# Which has the same effect when you call:
# easy.disconnect()
```

### Create table and insert a record

```python
from easypysql.easy import Table

class Student(Table):

    __table_name__ = "student"

    id = Field(Integer(), auto_increment=True)
    name = Field(String(), nullable=False)
    age = Field(Integer(), nullable=True, default=0)


easy.create_all()
```

To create a table, declare a class which inherits the Table class. It is strongly recommanded you to give the value of the `__table_name__`, the default value of it is the name of the class. Then the real table will be created if you call the `create(db_name1, db_name2, ...)` method, an easier way is using the `create_all()` like what i was do in the example.

```python
stu1 = Student(id=1, name="Justin", age=20)

easy.add(stu1)
```

Now let us create a instance of the Student, the value of age will be 0 if you don't provided. Like others, once you perform a DML action, one transaction will be initiated in default. That's to say, to make `stu1` become a record in your table, use the following function:

```python
easy.commit()
```

### Drop a table and delete a record

To drop a table, i design the same interface as you create a table: `drop(db_name1, db_name2, …)`, `drop_all()` One example is:

```python
class Student(Table):

    __table_name__ = 'student'

    id = Field(Integer(), auto_increment=True)
    name = Field(String(), nullable=False)
    age = Field(Integer(), nullable=True, default=0)


easy.create_all()

easy.drop_all()
```

When you run this code, The table student will be created first then be dropped. Of course you can use `easy.drop(Student)`

There're two way for you to delete a record, one is pass a a instance to `easy.delete(instance)`, the other is using the result you got from query method(The next part will introduce query).

There are two example using the both of them perspectively:

```python
stu = Student(name="Justin6", age=20)

easy.delete(stu)
```

```python
result = easy.query(Student).first()

easy.delete(result)
```

And believe you still remember, only when you manually call `easy.commit()` to make this change happen in your database. (Or change the transaction mode to auto_commit when you make easyconnect)

### Make a query

Now we have an record in the tmpdb.student, how to get it to use it?

```python
result = easy.query(Student)
print(result)
```

Using `query()` method to get a `Query` object, if you are only interested in one field, you can pass that field:

```python
result = easy.query(Student.name)
```

**Warning: Recommend to pass a Table object to query. Only this way can get the full support with Query.**

However, the result may not be the last result you want, you can get that through one of these: `first()`, `all()`, `one()`.

```python
result = easy.query(Student.name).first() # It is not recommended. Pass `Student` is better.
print(result)
```

The output is:

```python
('Justin',)
```

If the reasult set is `[]`. The `first()` will return `None` instead.

Like what you learnt from SQLAlchemy, `Query` object also support chaining call, like the following shows:

```python
result = easy.query(Student).order_by(Student.name).all()
```

If the result set is `[]`, The `all()` will return `[]`.

`order_by`is a sort method that will return a new `Query` object that contain a new result set which has the right sequence you want.

And also, `count()` will return the total number of the result set:

```python
length = easy.query(Student).count()
```

In this case, the value of `length` is `1`.

### Execute raw SQL

Also, easypysql allows you to pass raw SQL:

```python
easy.send('''SQL HERE''')
```

Actually, send is the `execute` method which is implemented by the connector.