# coding: utf-8


class Query(object):
    def __init__(self, result_set):
        self.pointer = -1
        self.table_map = None
        self.result = result_set

    def all(self):
        return self.result

    def first(self):
        return self.result[0]

    def one(self):
        self.pointer += 1
        return self.result[self.pointer]

    def count(self):
        return len(self.result)

    def filter(self, *args):
        pass

    def order_by(self, field, desc=False):
        if self.table_map is not None:
            if field.__class__.__name__ is not "Field":
                raise ValueError('Only Field can be ordered.')
            index = self.table_map.index(field.field_name)
            order_set = self.result.copy()
            order_set.sort(key=lambda x: x[index])
            if desc:
                order_set.reverse()
            return order_set
        else:
            raise ValueError('Only Table query can use order_by.')

    def set_table(self, table):
        self.table_map = table
