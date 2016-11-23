from utils import *
from bitarray import *
from collections import OrderedDict
from orderedset import OrderedSet

class Bitset(bitarray):

    """
    Rappresenta la sequenza di bit di una colonna della matrice.
    """

    def __hash__(self):
        return self.to01().__hash__()

class Matrix:

    """
    Rappresenta il concetto cardine del calcolo dei MHS.
    E' dotata di:
        > un insieme ordinato di bitarray che rappresentano le righe
        > un dizionario che mappa gli id delle colonne con i Bitset, rappresentanti le colonne stesse
        > un dizionario che mappa gli id delle colonne con il numero di 1 contenuti nelle stesse (euristica)
    """

    def __init__(self, rows=None, col_ids=None):

        """
        Inizializza la matrice a partire da una lista di stringhe che rappresentano le righe.
        """

        self.rows = OrderedSet()
        self.cols = OrderedDict()
        self.counter1_col = OrderedDict()
        if rows:
            for row in rows:
                self.rows.add(Bitset(row))
            self.create_cols(col_ids)
            self.update_counter1_col()
            # self.update_counter1_row()
        else:
            for col_id in col_ids:
                self.cols[col_id] = None

    def __str__(self):

        """
        Crea e restituisce una rappresentazione della matrice in forma testuale.
        """

        if self.is_empty():
            return 'Empty matrix'

        s = ' '.join(['%5s' % col_id for col_id in self.cols.keys()])
        s += '\n'
        for row in self.rows:
            s += ' '.join(['%5s' % bit for bit in row.to01()]) + '\n'
        return s

    def create_cols(self, col_ids):
        if not col_ids:
            col_ids = [str(i + 1) for i in range(len(self.rows[0]))]
        for i in range(len(self.rows[0])):
            for row in self.rows:
                try:
                    # self.cols['c' + str(i + 1)].append(Bitset(row[i]))
                    self.cols[col_ids[i]].append(Bitset(row[i]))
                except KeyError:
                    # self.cols['c' + str(i + 1)].append(Bitset(row[i]))
                    self.cols[col_ids[i]] = Bitset([row[i]])

    def add_row(self, row):
        self.rows.add(row)

    def is_empty(self):

        """
        Verifica se la matrice e' vuota, ovvero se e' priva di righe.
        """

        return len(self.rows) == 0

    def update_rows(self):

        """
        Aggiorna le righe eliminando in ognuna i bit nelle posizioni interessate dall'eventuale precedente eliminazione
        delle rispettive colonne.
        """

        rows = OrderedSet()
        if self.cols:
            for i in range(len(self.rows)):
                row = Bitset()
                for col in self.cols.values():
                    row.append(Bitset(col[i]))
                rows.add(row)
        self.rows = rows

    def update_cols(self):

        """
        Analogo a update_rows.
        Aggiorna le colonne eliminando in ognuna i bit nelle posizioni interessate dall'eventuale precedente
        eliminazione delle rispettive righe.
        """

        if not self.rows:
            self.cols = OrderedDict()
            return
        for col_id in self.cols.keys():
            self.cols[col_id] = Bitset()
        for row in self.rows:
            for i, col_id in enumerate(self.cols.keys()):
                self.cols[col_id].append(row[i])
        self.update_counter1_col()

    def update_counter1_col(self):

        """
        Aggiorna il contatore degli 1 delle colonne.
        """

        self.counter1_col = OrderedDict()
        for col_id, col in self.cols.iteritems():
            self.counter1_col[col_id] = int(col.count())

    # def update_counter1_row(self):
    #
    #     """
    #     Aggiorna il contatore degli 1 delle righe.
    #     """
    #
    #     self.counter1_row = []
    #     for i, row in enumerate(self.rows):
    #         self.counter1_row.append((i, int(row.count())))

    def submatrix(self, removed_rows=None, removed_cols=None):

        """
        Rimuove dalla matrice le righe e le colonne specificate.
        """

        rows = OrderedSet()
        cols = OrderedDict()
        if removed_rows:
            for i, row in enumerate(self.rows):
                if i not in removed_rows:
                    rows.add(row)

            self.rows = rows
            self.update_cols()
        if self.cols:
            if removed_cols:
                for col_id, col in self.cols.iteritems():
                    if col_id not in removed_cols:
                        cols[col_id] = col
                    # else:
                    #     self.counter1_col.pop(col_id)
                self.cols = cols
                self.update_rows()
                self.update_cols()
                # self.update_counter1_col()
        else:
            self.counter1_col = OrderedDict()

    def max_cols1(self):

        """
        Restituisce la lista degli id delle colonne contenenti il maggior numero di 1.
        """

        return max_cols1(self.counter1_col)

    def hit_rows(self, col_id):

        """
        Restituisce gli indici delle righe colpite da una colonna.
        """

        hit_rows = []
        for i, bit in enumerate(self.cols[col_id]):
            if bit:
                hit_rows.append(i)
        return hit_rows

    # def remove_super_sets(self):
    #     self.update_counter1_row()
    #     self.counter1_row = sorted(self.counter1_row, lambda x, y: x[1] - y[1])
    #     removed_rows = []
    #     while self.counter1_row:
    #         counter1_row = []
    #         row = self.rows[self.counter1_row.pop(0)[0]]
    #         for j in range(len(self.counter1_row)):
    #             if self.counter1_row[j][0] not in removed_rows:
    #                 if row & self.rows[self.counter1_row[j][0]] == row:
    #                     removed_rows.append(self.counter1_row[j][0])
    #                 else:
    #                     counter1_row.append(self.counter1_row[j])
    #         self.counter1_row = deepcopy(counter1_row)
    #     rows = OrderedSet()
    #     for i, row in enumerate(self.rows):
    #         if i not in removed_rows:
    #             rows.add(row)
    #     self.rows = rows
    #     self.update_counter1_row()
    #     self.update_cols()

    def remove_super_sets(self):
        i = 0
        while i < len(self.rows) - 1:
            j = i + 1
            while j < len(self.rows):
                if self.rows[i] & self.rows[j] == self.rows[j]:
                    self.rows.remove(self.rows[i])
                    j = i + 1
                elif self.rows[i] & self.rows[j] == self.rows[i]:
                    self.rows.remove(self.rows[j])
                else:
                    j += 1
            i += 1
        self.update_cols()

    def remove_cols_without_1(self):

        """
        Rimuove le colonne che non contengono alcun 1.
        Gli elementi corrispondenti alle colonne eliminate non appartengono ad alcun insieme.
        """

        cols = OrderedDict()
        for col_id, col in self.cols.iteritems():
            if col.any():
                cols[col_id] = col
            else:
                self.counter1_col.pop(col_id)
        self.cols = cols
        self.update_rows()

    def remove_duplicated_cols(self):

        """
        Rimuove le colonne duplicate.
        Gli elementi corrispondenti alle colonne eliminate sono in alternativa con quelli di cui si mantiene
        l'occorrenza.
        """

        occurrences = OrderedDict()
        for i, col_id1 in enumerate(self.counter1_col.keys()):
            count_ones_1 = self.counter1_col[col_id1]
            for col_id2 in self.counter1_col.keys()[i+1:]:
                count_ones_2 = self.counter1_col[col_id2]
                if count_ones_1 == count_ones_2:
                    if self.cols[col_id1] == self.cols[col_id2]:
                        occurrences[col_id1] = col_id2
                        break
        cols = OrderedDict()
        for col_id, col in self.cols.iteritems():
            if col_id not in occurrences.values():
                cols[col_id] = col
            else:
                self.counter1_col.pop(col_id)
        self.cols = cols
        self.update_rows()
        return occurrences

    def remove_cols_without_0(self):

        """
        Rimuove le colonne che non contengono alcuno 0.
        Gli elementi corrispondenti alle colonne eliminate rappresentano dei singoletti che devono essere memorizzati.
        """

        cols = OrderedDict()
        singletons = []
        for col_id, col in self.cols.iteritems():
            if col.all():
                singletons.append(col_id)
                self.counter1_col.pop(col_id)
            else:
                cols[col_id] = col
        self.cols = cols
        self.update_rows()
        return singletons

    def process_rows_with_unique_1(self):

        """
        Elabora le righe che contengono un unico 1.
        Gli elementi corrispondenti alle posizioni degli 1 appartengono a tutti i MHS, pertanto si possono eliminare le
        righe e le colonne interessate e memorizzare gli elementi cosi' trovati.
        """

        removed_rows = []
        removed_cols = []
        for i, row in enumerate(self.rows):
            if i not in removed_rows:
                if row.count() == 1:
                    col_index = int(row.index(True))
                    col_id = self.cols.keys()[col_index]
                    removed_cols.append(col_id)
                    # col = self.cols[col_id]
                    removed_rows.append(i)
                    # for j, bit in enumerate(col):
                    #     if bit and j not in removed_rows:
                    #         removed_rows.append(j)
        self.submatrix(removed_rows, removed_cols)
        return removed_cols

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
            submatrices = [Matrix(col_ids=self.cols.keys()) for _ in range(len(partitions))]
            for row in self.rows:
                for i, partition in enumerate(partitions):
                    if (row & partition).any():
                        submatrices[i].add_row(deepcopy(row))
                        break
            for submatrix in submatrices:
                submatrix.update_cols()
                submatrix.remove_cols_without_1()
        return submatrices

    def check_for_rows_without_1(self):

        """
        Controlla se ci sono righe composte da soli zeri.
        """

        for row in self.rows:
            if not row.any():
                return True
        return False

    def preprocessing(self):

        """
        Effettua il preprocessing in maniera iterativa, invocando uno dopo l'altro i metodi sopraelencati.
        Costruisce progressivamente l'espressione dei MHS.
        """

        old_dimension = (-1, -1)
        new_dimension = (len(self.rows), len(self.cols))
        occurrences_list = []
        everywhere_ids = []
        singletons = []
        while new_dimension != (0, 0) and old_dimension != new_dimension:
            old_dimension = new_dimension
            self.remove_cols_without_1()
            self.remove_super_sets()
            occurrences = self.remove_duplicated_cols()
            occurrences_list.append(occurrences)
            singletons.append(self.remove_cols_without_0())
            if not self.check_for_rows_without_1():
                everywhere_ids.append(self.process_rows_with_unique_1())
            else:
                everywhere_ids.append([])
            new_dimension = (len(self.rows), len(self.cols))
        substitutions_map = get_substitutions_map(occurrences_list)
        return singletons, everywhere_ids, substitutions_map

    def find_next_col(self, compl_cols):
        if not compl_cols:
            self.find_complementary_cols(compl_cols)
        tuples = map(lambda (k, v): (k, len(v)), compl_cols.iteritems())
        max_count_compl = max(tuples, key=lambda item: item[1])[1]
        col_ids = [tup[0] for i, tup in enumerate(tuples) if tup[1] == max_count_compl]
        if max_count_compl == 0:
            cols_to_consider = range(len(self.cols))
        else:
            if len(col_ids) == 1:
                cols_to_consider = [self.cols.keys().index(col_ids[0])]
            else:
                cols_to_consider = [self.cols.keys().index(x) for x in col_ids]
        col_id = self.cols.keys()[cols_to_consider[0]]
        count0 = self.count_0_hit_by_col(col_id)
        for i in cols_to_consider[1:]:
            new_col_id = self.cols.keys()[i]
            new_count0 = self.count_0_hit_by_col(new_col_id)
            if count0 < new_count0 or (count0 == new_count0 and self.counter1_col[col_id] < self.counter1_col[new_col_id]):
                col_id = new_col_id
                count0 = new_count0
        for compl_id in compl_cols.pop(col_id):
            compl_cols[compl_id].remove(col_id)
        return col_id

    def find_complementary_cols(self, compl_cols):
        for col_id in self.cols:
            compl_cols[col_id] = []
        for col_id_i, col_i in self.cols.iteritems():
            for col_id_j, col_j in self.cols.iteritems():
                if col_id_i != col_id_j and (col_i | col_j).all():
                    compl_cols[col_id_i].append(col_id_j)

    def count_0_hit_by_col(self, col_id):
        col = self.cols[col_id]
        count = 0
        for i in range(len(col)):
            if col[i]:
                count += self.rows[i].count(False)
        return count

    def to_json(self):
        json = '{\n\t"sets": [\n\t\t'
        sets = []
        for row in self.rows:
            _set = []
            for j, bit in enumerate(row):
                if bit:
                    _set.append(int(self.cols.keys()[j]))
            sets.append(_set)
        json += ',\n\t\t'.join([str(_set) for _set in sets])
        json += '\n\t]\n}'
        return json