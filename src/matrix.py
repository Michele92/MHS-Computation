"""Contiene le classi per rappresentare la matrice di input"""

from copy import deepcopy

from orderedset import OrderedSet

class Bitset(object):

    def __init__(self, bitstring=None, content=None):
        if content:
            self.content = content
        else:
            if not bitstring:
                bitstring = []
            self.content = []
            for bit in bitstring:
                self.content.append(bit == '1')

    def __hash__(self):
        return str(self).__hash__()

    def __len__(self):
        return len(self.content)

    def __getitem__(self, item):
        return self.content[item]

    def __eq__(self, other):
        return self.content.__eq__(other.content)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.to01()

    def append(self, item):
        self.content.append(item)

    def to01(self):
        result = ''
        for bit in self.content:
            result += '1' if bit else '0'
        return result

    def count(self, value=True):
        return self.content.count(value)

    def index(self, value=True):
        return self.content.index(value)

    def all(self):
        return all(self.content)

    def any(self):
        return any(self.content)

class Row(Bitset):

    def __init__(self, bitstring=None, content=None):
        super(Row, self).__init__(bitstring=bitstring, content=content)
        self.grey_level = 0

    def __and__(self, other):
        content = []
        for i in range(len(self.content)):
            content.append(self.content[i] and other.content[i])
        return Row(content=content)

    def __or__(self, other):
        content = []
        for i in range(len(self.content)):
            content.append(self.content[i] or other.content[i])
        return Row(content=content)

    def __ior__(self, other):
        for i in range(len(self.content)):
            self.content[i] = self.content[i] or other.content[i]
        return self

    def get_grey_level(self):
        return self.grey_level

    def set_grey_level(self, grey_level):
        self.grey_level = grey_level

class Column(Bitset):

    def __init__(self, bitstring=None, content=None, _id=None):
        super(Column, self).__init__(bitstring=bitstring, content=content)
        self._id = _id

    def __and__(self, other):
        content = []
        for i in range(len(self.content)):
            content.append(self.content[i] and other.content[i])
        return Column(content=content)

    def __or__(self, other):
        content = []
        for i in range(len(self.content)):
            content.append(self.content[i] or other.content[i])
        return Column(content=content)

    def get_id(self):
        return self._id

class Matrix:

    def __init__(self, rows=None, col_ids=None):
        self.rows = OrderedSet()
        self.cols = []
        if rows:
            for row in rows:
                self.rows.add(Row(bitstring=row))
            self.create_cols(col_ids)
        else:
            for col_id in col_ids:
                self.cols.append(Column(_id=col_id))

    def __str__(self):
        if self.is_empty():
            return 'Empty matrix'
        s = ' '.join(['%5s' % col.get_id() for col in self.cols]) + '\n'
        for row in self.rows:
            s += ' '.join(['%5s' % bit for bit in str(row)]) + '\n'
        return s

    def get_cols(self):
        return self.cols

    def get_col_by_id(self, col_id):
        for col in self.cols:
            if col.get_id() == col_id:
                return col
        return None

    def add_row(self, row):
        self.rows.add(row)

    def create_cols(self, col_ids):
        if not col_ids:
            col_ids = [str(i + 1) for i in range(len(self.rows[0]))]
        for i in range(len(self.rows[0])):
            col = Column(_id=col_ids[i])
            for row in self.rows:
                col.append(row[i])
            self.cols.append(col)

    def is_empty(self):
        return len(self.rows) == 0

    def update_rows(self):
        if not self.cols:
            self.rows = OrderedSet()
            return
        rows = OrderedSet()
        for i in range(len(self.rows)):
            row = Row()
            for col in self.cols:
                row.append(col[i])
            rows.add(row)
        self.rows = rows

    def update_cols(self):
        if not self.rows:
            self.cols = []
            return
        cols = []
        for i in range(len(self.cols)):
            col_id = self.cols[i].get_id()
            col = Column(_id=col_id)
            for row in self.rows:
                col.append(row[i])
            cols.append(col)
        self.cols = cols

    def submatrix(self, removed_rows=None, removed_cols=None):
        rows = OrderedSet()
        cols = []
        if removed_rows:
            for i, row in enumerate(self.rows):
                if i not in removed_rows:
                    rows.add(row)
            self.rows = rows
            self.update_cols()
        if self.cols:
            if removed_cols:
                for i, col in enumerate(self.cols):
                    if i not in removed_cols:
                        cols.append(col)
                self.cols = cols
                self.update_rows()
                self.update_cols()

    def max_grey_level(self):
        result = self.rows[0].get_grey_level()
        for i in range(1, len(self.rows)):
            row = self.rows[i]
            if row.get_grey_level() > result:
                result = row.get_grey_level()
        return result

    def get_grey_scale_count(self):
        grey_scale_count = {}
        for row in self.rows:
            grey_level = row.get_grey_level()
            if grey_level in grey_scale_count:
                grey_scale_count[grey_level] += 1
            else:
                grey_scale_count[grey_level] = 1
        return grey_scale_count

    def check_for_hit_grey_rows(self, col_id):
        grey_scale_count = self.get_grey_scale_count()
        removed_rows = []
        col = self.get_col_by_id(col_id)
        for i, bit in enumerate(col):
            if bit:
                if self.rows[i].get_grey_level() > 0:
                    removed_rows.append(i)
                grey_level = self.rows[i].get_grey_level()
                grey_scale_count[grey_level] -= 1
                if grey_scale_count[grey_level] == 0:
                    if grey_level != 0:
                        return True
        self.submatrix(removed_rows=removed_rows)
        return False

    def set_grey_rows(self, col_id):
        new_grey_level = self.max_grey_level() + 1
        col = self.get_col_by_id(col_id)
        for i, bit in enumerate(col):
            if bit:
                self.rows[i].set_grey_level(new_grey_level)

    def hit_rows(self, col_index):
        hit_rows = []
        col = self.cols[col_index]
        for i, bit in enumerate(col):
            if bit:
                hit_rows.append(i)
        return hit_rows

    def remove_redundant_rows(self):
        i = 0
        while i < len(self.rows) - 1:
            j = i + 1
            while j < len(self.rows):
                if (self.rows[i] & self.rows[j]) == self.rows[i]:
                    self.rows.remove(self.rows[j])
                elif (self.rows[i] & self.rows[j]) == self.rows[j]:
                    self.rows.remove(self.rows[i])
                    j = i + 1
                else:
                    j += 1
            i += 1
        self.update_cols()

    def remove_equals_cols(self):
        substitutions_map = {}
        i = 0
        while i < len(self.cols) - 1:
            col_i = self.cols[i]
            j = i + 1
            while j < len(self.cols):
                col_j = self.cols[j]
                if col_i == col_j:
                    if col_i.get_id() in substitutions_map:
                        substitutions_map[col_i.get_id()].append(col_j.get_id())
                    else:
                        substitutions_map[col_i.get_id()] = [col_j.get_id()]
                    self.cols.pop(j)
                else:
                    j += 1
            i += 1
        self.update_rows()
        return substitutions_map

    def process_cols(self, remove_singletons=True):
        singletons = []
        i = 0
        while i < len(self.cols):
            if not self.cols[i].any():
                self.cols.pop(i)
            elif remove_singletons and self.cols[i].all():
                singletons.append(self.cols[i].get_id())
                self.cols.pop(i)
            else:
                i += 1
        self.update_rows()
        return singletons

    def process_rows_with_unique_1(self):
        removed_rows = []
        removed_cols = []
        everywhere_ids = []
        for i, row in enumerate(self.rows):
            if i not in removed_rows:
                if row.count() == 1:
                    col_index = int(row.index(True))
                    removed_cols.append(col_index)
                    everywhere_ids.append(self.cols[col_index].get_id())
                    removed_rows.append(i)
        self.submatrix(removed_rows, removed_cols)
        return everywhere_ids

    def get_super_cols(self, col_index):
        input_col = self.cols[col_index]
        super_cols = []
        for i, col in enumerate(self.cols):
            if i != col_index:
                if (col & input_col) == input_col:
                    super_cols.append(i)
        return super_cols

    def check_for_rows_without_1(self):
        for row in self.rows:
            if not row.any():
                return True
        return False

    def partition(self):
        partitions = [deepcopy(self.rows[0])]
        for i in range(1, len(self.rows)):
            matching_partitions = []
            for j in range(len(partitions)):
                if (self.rows[i] & partitions[j]).any():
                    partitions[j] |= self.rows[i]
                    matching_partitions.append(j)
            if not matching_partitions:
                partitions.append(deepcopy(self.rows[i]))
            else:
                new_partition = deepcopy(partitions[matching_partitions[0]])
                for k in matching_partitions[1:]:
                    new_partition |= partitions[k]
                partitions = filter(lambda p: partitions.index(p) not in matching_partitions, partitions)
                partitions.append(new_partition)
        submatrices = None
        if len(partitions) > 1:
            col_ids = map(lambda col: col.get_id(), self.cols)
            submatrices = [Matrix(col_ids=col_ids) for _ in range(len(partitions))]
            for row in self.rows:
                for i, partition in enumerate(partitions):
                    if (row & partition).any():
                        submatrices[i].add_row(deepcopy(row))
                        break
            for submatrix in submatrices:
                submatrix.update_cols()
                submatrix.process_cols(remove_singletons=False)
        return submatrices

    def preprocessing(self, enable_map):
        old_size = (-1, -1)
        new_size = (len(self.rows), len(self.cols))
        singletons = []
        everywhere_ids = []
        self.remove_redundant_rows()
        substitution_map = None
        if enable_map:
            substitution_map = self.remove_equals_cols()
        while new_size != (0, 0) and new_size != old_size:
            old_size = new_size
            singletons.append(self.process_cols())
            if not self.check_for_rows_without_1():
                everywhere_ids.append(self.process_rows_with_unique_1())
            else:
                everywhere_ids.append([])
            new_size = (len(self.rows), len(self.cols))
        return singletons, everywhere_ids, substitution_map

    def find_next_col(self):
        for row in self.rows:
            if row.count() == 1:
                return row.index()
        # return 0
        zero_counters = [self.count_0_hit_by_col(col_index) for col_index in range(len(self.cols))]
        return zero_counters.index(max(zero_counters))
        # one_counters = [self.cols[i].count() for i in range(len(self.cols))]
        # return one_counters.index(max(one_counters))

    def count_0_hit_by_col(self, col_index):
        # col = self.cols[col_index]
        # count = 0
        # for i in range(len(col)):
        #     if col[i]:
        #         count += self.rows[i].count(False)
        # return count
        col = self.cols[col_index]
        first_one_index = col.index(True)
        max_count = self.rows[first_one_index].count(False)
        for i in range(first_one_index + 1, len(col)):
            if col[i]:
                count = self.rows[i].count(False)
                if count > max_count:
                    max_count = count
        return max_count

    def to_sets(self):
        sets = []
        for row in self.rows:
            _set = set()
            for j, bit in enumerate(row):
                if bit:
                    _set.add(self.cols[j].get_id())
            sets.append(_set)
        return sets
