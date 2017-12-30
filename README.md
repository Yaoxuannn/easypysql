# Easypysql

This is a simple and small ORM micro-framework implements with Python3, which is mainly for check myself. Here is a simple introduction of it and the instruction for using. (Of course i know nobody will give it a shit, please **DO NOT USE IT IN THE PRODUCTION ENV.**)

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

All Object-SQL transform are done in the `mapper.sqlmapping`. (What an ugly design!)

The url module is more like a util module, I write this module (And i learnt some regular expression from SQLalchemy.) to support URL-connect method, and modified the component which i will show you in the next part of this article.

## Instruction

I can make sure that no one will look this part as nobody will use this toy, even try it. :) 

I name this ORM cake **`easypysql`**, that means it is easy to use. Additionally, only use it in a easy condition.

As you learnt in the introduction part, the core module is `easy.Easy`. So, how to get it?

```python
from easypysql.easy import easyconnect, ConnectionException

path = '/tmp/tmpdb'

try:
    easy = easyconnect("sqlite:///%s" % path, timeout=10)
except ConnectionException:
    pass
```

the method `easyconnect` has an alias as `connect`, which has the exactly same effect of the former. This action is for someone who dont't like the name of `easyconnect`. As this method called, an connection will be established.

Now you can use easy to do some cool things!

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

Now we have an record in the tmpdb.student, how to get it to use it?

```python
result = easy.query(Student)
print(result)
```

Using `query()` method to get a `Query` object, if you are only interested in one field, you can pass that field:

```python
result = easy.query(Student.name)
```

However, the result may not be the last result you want, you can get that through one of these: `first()`, `all()`, `one()`.

```python
result = easy.query(Student.name).first()
print(result)
```

The output is:

```python
('Justin',)
```

The diffrent between `first()` and `one()` is later has a behavior like a generator(Actually not), you will get the next value each time call this.

