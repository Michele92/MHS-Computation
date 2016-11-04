# import os
from copy import deepcopy

def reverse_dict(d):
    reversed_dict = {}
    for key, value in d.iteritems():
        reversed_dict[value] = key
    return reversed_dict

def get_substitutions_map(occurrences_list):
    substitutions_map = {}
    for occurrences in occurrences_list:
        occurrences_old = deepcopy(occurrences)
        occurrences_rev = reverse_dict(occurrences)
        keys = []
        while occurrences:
            key, value = occurrences.popitem(0)
            if key in substitutions_map:
                _key = value
                substitutions_map[key].append(_key)
                while _key in occurrences:
                    substitutions_map[key].append(occurrences[_key])
                    _key = occurrences.pop(_key)
                if key in occurrences_rev:
                    _key = occurrences_rev.pop(key)
                    substitutions_map[key].append(_key)
                    while _key in occurrences_rev:
                        substitutions_map[key].append(occurrences_rev[_key])
                        _key = occurrences_rev.pop(_key)
            else:
                keys.append(key)
        while keys:
            key = keys.pop(0)
            values = []
            for value_list in substitutions_map.values():
                values += value_list
            if key not in values:
                substitutions_map[key] = []
                _key = occurrences_old.pop(key)
                substitutions_map[key].append(_key)
                while _key in occurrences_old:
                    substitutions_map[key].append(occurrences_old[_key])
                    _key = occurrences_old.pop(_key)
    return substitutions_map

def max_cols1(counter1):
    col_ids = []
    max_value = -1
    for col_id, value in counter1.iteritems():
        if value > max_value:
            col_ids = [col_id]
        elif value == max_value:
            col_ids.append(col_id)
    return col_ids

def compute_mhs(matrix, removed_rows=[]):

    """
    Completa il calcolo dei MHS elaborando una colonna ad ogni iterazione.
    In ciascuna iterazione si elimina una colonna e le righe in cui compare un 1 e si effettua il preprocessing
    sulla sottomatrice cosi' ottenuta.
    """
    matrix.submatrix(removed_rows=removed_rows)
    result = None
    while not matrix.check_for_empty_rows():
        singletons, everywhere_ids, substitutions_map = matrix.preprocessing()
        mhs_expr = '+'.join(singletons)
        if everywhere_ids:
            mhs_expr += '+' + ''.join(everywhere_ids)
        max_col_ids = matrix.max_cols1()
        col_id = max_col_ids.pop()
        hit_rows = matrix.hit_rows(col_id)
        matrix.submatrix(removed_cols=[col_id])
        result = compute_mhs(deepcopy(matrix), hit_rows)
        if result is not None:

    return result

# def create_dir(dirname):
#     if not os.path.exists(dirname):
#         os.makedirs(dirname)
#     return dirname + '/'

# def show_progress(fname, partial, total):
#     progress = int(round(100 * float(partial) / total))
#     os.system('cls')
#     print fname + ': progress: ' + str(progress) + '% (' + str(partial) + '/' + str(total) + ')'