# coding: utf-8


class Query(object):
    def __init__(self, result_set):
        self.pointer = -1
        self.table = None
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

    def order_by(self, field):
        pass

    def set_table(self, table):
        self.table = table
