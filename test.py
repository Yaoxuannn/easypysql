from easypysql.easy import easyconnect, Table, ConnectionException
from easypysql.sql.types import Field, Integer, String

path = "/tmp/tmpdb"
easy = None

try:
    easy = easyconnect("sqlite:///%s" % path, timeout=10)
except ConnectionException:
    pass


class Student(Table):

    # __table_name__ = 'student'

    id = Field(Integer(), auto_increment=True)
    name = Field(String(), nullable=False)
    age = Field(Integer(), nullable=True, default=0)


easy.create_all()

stu1 = Student(id=4, name="Justin4", age=21)

easy.add(stu1)
# easy.commit()

result = easy.query(Student).order_by(Student)
# easy.query(Student).first()

print(result)
