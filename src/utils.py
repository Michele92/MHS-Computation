# import os
from copy import deepcopy
from expression import *

def reverse_dict(d):

    """
    Restituisce un dizionario avente chiavi e valori scambiati rispetto a quello passato come parametro.
    """

    reversed_dict = {}
    for key, value in d.iteritems():
        reversed_dict[value] = key
    return reversed_dict

def get_substitutions_map(occurrences_list):

    """
    Determina la mappa delle sostituzioni delle colonne.
    Restituisce un dizionario le cui chiavi sono gli id delle colonne di cui si tiene l'istanza e i valori sono liste
    di id delle colonne duplicate.
    """

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

    """
    Restituisce la lista di chiavi di un dizionario aventi i valori massimi.
    """

    col_ids = []
    max_value = -1
    for col_id, value in counter1.iteritems():
        if value > max_value:
            col_ids = [col_id]
            max_value = value
        elif value == max_value:
            col_ids.append(col_id)
    return col_ids

def compute_mhs(matrix, removed_col=None, removed_rows=[], i=0):

    """
    Completa il calcolo dei MHS elaborando una colonna ad ogni iterazione.
    In ciascuna iterazione si elimina una colonna e le righe in cui compare un 1 e si effettua il preprocessing
    sulla sottomatrice cosi' ottenuta.
    """

    if removed_col:
        matrix.submatrix(removed_rows=removed_rows)
        matrix.submatrix(removed_cols=[removed_col])
    singletons, everywhere_ids, substitutions_map = matrix.preprocessing()
    result = None
    while not matrix.is_empty() and not matrix.check_for_rows_without_1():
        mhs_expr = '+'.join(singletons)
        if everywhere_ids:
            mhs_expr += '+' + ''.join(everywhere_ids)
        max_col_ids = matrix.max_cols1()
        if matrix.cols:
            col_id = max_col_ids.pop(0)
            hit_rows = matrix.hit_rows(col_id)
            result = compute_mhs(deepcopy(matrix), col_id, hit_rows, i+1)
            matrix.submatrix(removed_cols=[col_id])
    return result

def generate_expression(singletons, everywhere_ids, substitutions_map):

    """
    Genera un'espressione temporanea sulla base dei singoletti, degli id degli elementi appartenenti a tutti i mhs del
    contesto attuale e della mappa delle sostituzioni.
    """
    singletons, everywhere_ids = substitute(singletons, everywhere_ids, substitutions_map)
    expr = None
    for i in range(len(singletons)-1, -1, -1):
        prod = ProdExpression()
        if expr:
            prod.add_operand(expr)
        if everywhere_ids[i]:
            prod += ProdExpression([e for e in everywhere_ids[i]])
        if singletons[i]:
            expr = SumExpression([s for s in singletons[i]])
            if not prod.is_empty():
                expr.add_operand(prod)
        elif not prod.is_empty():
            expr = prod
    return expr

def substitute(singletons, everywhere_ids, substitutions_map):

    """
    Effettua la sostituzione degli id nei singoletti e negli elementi appartenenti a tutti i mhs del contesto attuale,
    sfruttando la mappa delle sostituzioni.
    """

    s = do_substitution(singletons, substitutions_map)
    e = do_substitution(everywhere_ids, substitutions_map)
    return s, e

def do_substitution(elems, substitutions_map):

    """
    Sostituisce gli elementi di una lista con le espressioni corrispondenti, sulla base della mappa delle sostituzioni.
    """

    s = []
    for i in range(len(elems)):
        ss = []
        if elems[i]:
            for elem in elems[i]:
                tmp = [AtomicElem(elem)]
                if elem in substitutions_map:
                    tmp += [AtomicElem(e) for e in substitutions_map[elem]]
                    ss.append(SumExpression(tmp))
                else:
                    ss.append(tmp[0])
        s.append(ss)
    return s

# def create_dir(dirname):
#     if not os.path.exists(dirname):
#         os.makedirs(dirname)
#     return dirname + '/'

# def show_progress(fname, partial, total):
#     progress = int(round(100 * float(partial) / total))
#     os.system('cls')
#     print fname + ': progress: ' + str(progress) + '% (' + str(partial) + '/' + str(total) + ')'