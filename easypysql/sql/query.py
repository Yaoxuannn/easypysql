# coding: utf-8


class Query(object):
    def __init__(self, result_set):
        self.table = None
        self.table_map = None
        self.result = result_set
        self.raw_result = result_set

    def all(self):
        return self.result

    def first(self):
        return self.result[0] if self.result else None

    def count(self):
        return len(self.result)

    def filter(self, *args):
        filter_set = []
        for item in self.result:
            flag = True
            for rule in args:
                if not self._filter(item, rule):
                    flag = False
            if flag:
                filter_set.append(item)
        return self._pack_query(filter_set)

    @staticmethod
    def _filter(result, rule):
        value = result.get(rule[0])
        other = rule[2]
        return eval("%s%s%s" % (value, rule[1], other))

    def _pack_query(self, result_set):
        q = Query(self._unpack_query(result_set))
        q.set_table(self.table, self.table_map)
        return q

    def order_by(self, field, desc=False):
        if self.table_map is not None:
            if field.__class__.__name__ is not "Field":
                raise ValueError('Only Field can be ordered.')
            order_set = self.result.copy()
            order_set.sort(key=lambda x: x.get(field.field_name))
            if desc:
                order_set.reverse()
            return self._pack_query(order_set)
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
