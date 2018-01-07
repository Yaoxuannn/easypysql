from easypysql.easy import easyconnect, Table, ConnectionException
from easypysql.sql.types import Field, Integer, String
from faker import Factory
from random import randint


f = Factory().create()
path = ":memory:"
easy = None

try:
    easy = easyconnect("sqlite:///%s" % path, timeout=10)
except ConnectionException:
    pass


class Student(Table):
    __table_name__ = 'student'

    id = Field(Integer(), auto_increment=True)
    name = Field(String(), nullable=False)
    age = Field(Integer(), nullable=True, default=0)


easy.create_all()

for n in range(100):
    stu = Student(name=f.name(), age=randint(16, 32))
    easy.add(stu)

easy.commit()

re = easy.query(Student)\
    .filter(Student.id > 1, Student.age > 20)\
    .order_by(Student.age, desc=True)\
    .all()


print(re)

easy.drop_all()

easy.close()
