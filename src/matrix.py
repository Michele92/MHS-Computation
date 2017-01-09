"""Contiene le classi per rappresentare la matrice di input"""

from collections import OrderedDict

from bitarray import *
from orderedset import OrderedSet

class CustomSet(OrderedSet):

    """Classe wrapper utile per il debug"""

    def __repr__(self):
        return '{' + ', '.join([repr(self.__getitem__(i)) for i in range(len(self))]) + '}'

class CustomList(list):

    """Classe wrapper utile per il debug"""

    def __repr__(self):
        return '[' + ', '.join([repr(self.__getitem__(i)) for i in range(len(self))]) + ']'

class Bitset(bitarray):

    """Classe wrapper che rappresenta un vettore di valori binari"""

    def __hash__(self):
        return self.to01().__hash__()

class Row:

    """
    Rappresenta una riga della matrice.
    E' caratterizzata dai seguenti attributi:
        - bitset, la sequenza di valori binari contenuti nella riga
        - grey_level, il livello di grigio associato alla riga
    """

    def __init__(self, bitset=None, grey_level=0):
        self.bitset = bitset
        if not bitset:
            self.bitset = Bitset()
        self.grey_level = grey_level

    def __hash__(self):
        return self.bitset.__hash__()

    def __len__(self):
        return len(self.bitset)

    def __getitem__(self, item):
        return self.bitset[item]

    def __and__(self, other):
        return Row(bitset=self.bitset & other.bitset)

    def __or__(self, other):
        return Row(bitset=self.bitset | other.bitset)

    def __ior__(self, other):
        self.bitset |= other.bitset
        return self

    def __eq__(self, other):
        return self.bitset == other.bitset

    def __ne__(self, other):
        return self.bitset != other.bitset

    def __str__(self):
        return self.bitset.to01()

    def __repr__(self):
        return self.bitset.to01() + ' [' + str(self.grey_level) + ']'

    def get_grey_level(self):
        return self.grey_level

    def set_grey_level(self, grey_level):
        self.grey_level = grey_level

    def append(self, item):
        return self.bitset.append(item)

    def count(self, value=True):
        return self.bitset.count(value)

    def index(self, value):
        return self.bitset.index(value)

    def any(self):
        return self.bitset.any()

    def all(self):
        return self.bitset.all()

class Column:

    """
    Rappresenta una colonna della matrice.
    E' caratterizzata dai seguenti attributi:
        - _id, l'identificatore associato alla colonna
        - bitset, la sequenza di valori binari contenuti nella colonna
    """

    def __init__(self, _id=None, bitset=None):
        self._id = _id
        self.bitset = bitset
        if not bitset:
            self.bitset = Bitset()

    def __len__(self):
        return len(self.bitset)

    def __getitem__(self, item):
        return self.bitset[item]

    def __and__(self, other):
        return Column(bitset=self.bitset & other.bitset)

    def __or__(self, other):
        return Column(bitset=self.bitset | other.bitset)

    def __eq__(self, other):
        return self.bitset == other.bitset

    def __ne__(self, other):
        return self.bitset != other.bitset

    def __str__(self):
        return self.bitset.to01()

    def __repr__(self):
        return '[' + self._id + '] ' + self.bitset.to01()

    def get_id(self):
        return self._id

    def append(self, item):
        return self.bitset.append(item)

    def count(self, value=True):
        return self.bitset.count(value)

    def any(self):
        return self.bitset.any()

    def all(self):
        return self.bitset.all()

class Matrix:

    """
    Rappresenta la matrice di input.
    E' caratterizzata dai seguenti attributi:
        - rows, l'insieme ordinato di righe
        - cols, la lista di colonne
    """

    def __init__(self, rows=None):
        self.rows = CustomSet()
        self.cols = CustomList()
        self.counter1_col = OrderedDict()
        if rows:
            for row in rows:
                self.rows.add(Row(bitset=Bitset(row)))
            self.create_cols()
            self.update_counter1_col()

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

    def create_cols(self):
        col_ids = [str(i+1) for i in range(len(self.rows[0]))]
        for i in range(len(self.rows[0])):
            bitset = Bitset()
            for row in self.rows:
                bitset.append(row[i])
            self.cols.append(Column(col_ids[i], bitset))

    def is_empty(self):
        return len(self.rows) == 0

    def update_rows(self):
        if not self.cols:
            self.rows = CustomSet()
            return
        rows = CustomSet()
        for i in range(len(self.rows)):
            bitset = Bitset()
            for col in self.cols:
                bitset.append(col[i])
            rows.add(Row(bitset))
        self.rows = rows

    def update_cols(self):
        if not self.rows:
            self.cols = CustomList()
            return
        cols = CustomList()
        for i in range(len(self.cols)):
            col_id = self.cols[i].get_id()
            bitset = Bitset()
            for row in self.rows:
                bitset.append(row[i])
            cols.append(Column(col_id, bitset))
        self.cols = cols
        self.update_counter1_col()

    def update_counter1_col(self):
        self.counter1_col = OrderedDict()
        for col in self.cols:
            self.counter1_col[col.get_id()] = int(col.count())

    def submatrix(self, removed_rows=None, removed_cols=None):
        rows = CustomSet()
        cols = CustomList()
        if removed_rows:
            for i, row in enumerate(self.rows):
                if i not in removed_rows:
                    rows.add(row)
            self.rows = rows
            self.update_cols()
        if self.cols:
            if removed_cols:
                for col in self.cols:
                    if col.get_id() not in removed_cols:
                        cols.append(col)
                self.cols = cols
                self.update_rows()
                self.update_cols()
        else:
            self.counter1_col = OrderedDict()

    def max_grey_level(self):
        result = self.rows[0].get_grey_level()
        for i in range(1, len(self.rows)):
            if self.rows[i].get_grey_level() > result:
                result = self.rows[i].get_grey_level()
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

    def hit_rows(self, col_id):
        hit_rows = []
        col = self.get_col_by_id(col_id)
        for i, bit in enumerate(col):
            if bit:
                hit_rows.append(i)
        return hit_rows

    def remove_super_sets(self):
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

    def process_cols(self):
        singletons = []
        i = 0
        while i < len(self.cols):
            if not self.cols[i].any():
                self.cols.pop(i)
            elif self.cols[i].all():
                singletons.append(self.cols[i].get_id())
                self.cols.pop(i)
            else:
                i += 1
        self.update_rows()
        return singletons

    def process_rows_with_unique_1(self):
        removed_rows = []
        removed_cols = []
        for i, row in enumerate(self.rows):
            if i not in removed_rows:
                if row.count() == 1:
                    col = self.cols[int(row.index(True))]
                    removed_cols.append(col.get_id())
                    removed_rows.append(i)
        self.submatrix(removed_rows, removed_cols)
        return removed_cols

    def get_super_cols(self, col_id):
        input_col = self.get_col_by_id(col_id)
        super_cols = []
        for col in self.cols:
            if col.get_id() != col_id:
                if (col & input_col) == input_col:
                    super_cols.append(col.get_id())
        return super_cols

    def check_for_rows_without_1(self):
        for row in self.rows:
            if not row.any():
                return True
        return False

    def preprocessing(self):
        old_dimension = (-1, -1)
        new_dimension = (len(self.rows), len(self.cols))
        singletons = []
        everywhere_ids = []
        self.remove_super_sets()
        while new_dimension != (0, 0) and new_dimension != old_dimension:
            old_dimension = new_dimension
            singletons.append(self.process_cols())
            if not self.check_for_rows_without_1():
                everywhere_ids.append(self.process_rows_with_unique_1())
            else:
                everywhere_ids.append([])
            new_dimension = (len(self.rows), len(self.cols))
        return singletons, everywhere_ids

    def find_next_col(self, complementary_cols):
        if not complementary_cols:
            complementary_cols = self.find_complementary_cols()
        complementary_cols_count = map(lambda (k, v): (k, len(v)), complementary_cols.iteritems())
        max_count = max(complementary_cols_count, key=lambda item: item[1])[1]
        col_ids = [count[0] for count in complementary_cols_count if count[1] == max_count]
        if max_count == 0:
            cols_to_consider = range(len(self.cols))
        else:
            cols_to_consider = [self.cols.index(self.get_col_by_id(col_id)) for col_id in col_ids]
        col_id = self.cols[cols_to_consider[0]].get_id()
        count0 = self.count_0_hit_by_col(col_id)
        for i in cols_to_consider[1:]:
            new_col_id = self.cols[i].get_id()
            new_count0 = self.count_0_hit_by_col(new_col_id)
            if count0 < new_count0 or (count0 == new_count0 and self.counter1_col[col_id] < self.counter1_col[new_col_id]):
                col_id = new_col_id
                count0 = new_count0
        for complementary_col_id in complementary_cols.pop(col_id):
            complementary_cols[complementary_col_id].remove(col_id)
        return col_id

    def find_complementary_cols(self):
        complementary_cols = OrderedDict()
        for col in self.cols:
            complementary_cols[col.get_id()] = []
        for col_i in self.cols:
            for col_j in self.cols:
                if col_i.get_id() != col_j.get_id() and (col_i | col_j).all():
                    complementary_cols[col_i.get_id()].append(col_j.get_id())
        return complementary_cols

    def count_0_hit_by_col(self, col_id):
        col = self.get_col_by_id(col_id)
        count = 0
        for i in range(len(col)):
            if col[i]:
                count += self.rows[i].count(False)
        return count

    def to_sets(self):
        sets = []
        for row in self.rows:
            _set = set()
            for j, bit in enumerate(row):
                if bit:
                    _set.add(self.cols[j].get_id())
            sets.append(_set)
        return sets
