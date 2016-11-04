from utils import *
from bitarray import *
from collections import OrderedDict
from orderedset import OrderedSet
from copy import deepcopy

class Bitset(bitarray):

    def __hash__(self):
        return self.to01().__hash__()

class Matrix:

    """
    Rappresenta il concetto cardine del calcolo dei MHS.
    E' dotata di un insieme ordinato di bitarray che rappresentano le righe e di un dizionario che mappa gli id delle
    colonne con i bitarray, rappresentanti le colonne stesse.
    """

    def __init__(self, rows):

        """
        Inizializza la matrice a partire da una lista di stringhe che rappresentano le righe.
        """

        self.rows = OrderedSet()
        for row in rows:
            self.rows.add(Bitset(row))
        self.cols = OrderedDict()
        for i in range(len(self.rows[0])):
            for row in self.rows:
                try:
                    self.cols['c' + str(i + 1)].append(Bitset(row[i]))
                except KeyError:
                    self.cols['c' + str(i + 1)] = Bitset([row[i]])
        self.counter1_col = OrderedDict()
        for col_id, col in self.cols.iteritems():
            self.counter1_col[col_id] = int(col.count())

    def __str__(self):

        """
        Crea e ritorna una rappresentazione della matrice in forma di stringa.
        """

        s = ' '.join(['%15s' % col_id for col_id in self.cols.keys()])
        s += '\n'
        for row in self.rows:
            s += ' '.join(['%15s' % bit for bit in row.to01()]) + '\n'
        return s

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
                self.cols[col_id].append(Bitset(row[i]))
        self.update_counter1()

    def update_counter1(self):
        self.counter1_col = OrderedDict()
        for col_id, col in self.cols.iteritems():
            self.counter1_col[col_id] = int(col.count())

    def submatrix(self, removed_rows=[], removed_cols=[]):
        rows = OrderedSet()
        cols = OrderedDict()
        if removed_rows:
            for i, row in enumerate(self.rows):
                if i not in removed_rows:
                    rows.add(row)
            self.rows = rows
            self.update_cols()

        if removed_cols:
            for col_id, col in self.cols.iteritems():
                if col_id not in removed_cols:
                    cols[col_id] = col
                else:
                    self.counter1_col.pop(col_id)
            self.cols = cols
            self.update_rows()

    def max_cols1(self):
        return max_cols1(self.counter1_col)

    def hit_rows(self, col_id):
        hit_rows = []
        for i, bit in enumerate(self.cols[col_id]):
            if bit:
                hit_rows.append(i)
        return hit_rows

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
        Gli elementi corrispondenti alle colonne eliminate sono in alternativa con quelli di cui si mantiene una sola
        occorrenza.
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
                    col = self.cols[col_id]
                    for j, bit in enumerate(col):
                        if bit and j not in removed_rows:
                            removed_rows.append(j)
        self.submatrix(removed_rows, removed_cols)
        return removed_cols

    def check_for_rows_without_1(self):
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
        while old_dimension != new_dimension:
            old_dimension = new_dimension
            self.remove_cols_without_1()
            occurrences = self.remove_duplicated_cols()
            occurrences_list.append(occurrences)
            singletons = self.remove_cols_without_0()
            everywhere_ids = self.process_rows_with_unique_1()
            new_dimension = (len(self.rows), len(self.cols))
        substitutions_map = get_substitutions_map(occurrences_list)
        return singletons, everywhere_ids, substitutions_map

    def compute_mhs(self, removed_rows=[]):

        """
        Completa il calcolo dei MHS elaborando una colonna ad ogni iterazione.
        In ciascuna iterazione si elimina una colonna e le righe in cui compare un 1 e si effettua il preprocessing
        sulla sottomatrice cosi' ottenuta.
        """

        if not self.check_for_empty_rows():
            for row in reversed(removed_rows):
                self.rows.remove(self.rows[row])
            self.update_cols()
            singletons, everywhere_ids, substitutions_map = self.preprocessing()
            max_col_ids = max_cols1(self.counter1_col)
            col_id = max_col_ids.pop()
            col = self.cols.pop(col_id)
            hit_rows = []
            for i, bit in enumerate(col):
                if bit:
                    hit_rows.append(i)
