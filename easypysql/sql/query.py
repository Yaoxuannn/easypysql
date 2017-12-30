# coding: utf-8


class Query(object):
    def __init__(self, result_set):
        self.pointer = -1
        self.table = None
        self.table_map = None
        self.result = []
        self.raw_result = result_set

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
            order_set = self.result.copy()
            order_set.sort(key=lambda x: x.get(field.field_name))
            print(order_set)
            if desc:
                order_set.reverse()
            q = Query(self._unpack_query(order_set))
            q.set_table(self.table, self.table_map)
            return q
        else:
            raise ValueError('Only Table query can use order_by.')

    def set_table(self, table, table_map):
        self.table = table
        self.table_map = table_map
        self.result = self._build_result_set()

    def _build_result_set(self):
        return [self.table(**dict(zip(self.table_map, item))) for item in self.raw_result]

    @staticmethod
    def _unpack_query(query_list):
        return [item.values() for item in query_list]
