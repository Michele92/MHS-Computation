import os
from collections import OrderedDict
from copy import deepcopy

from expression import *

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


def compute_mhs(matrix, original_matrix=None, removed_cols=None, removed_rows=None):
    """
    Completa il calcolo dei MHS elaborando una colonna ad ogni iterazione.
    In ciascuna iterazione si elimina una colonna e le righe in cui compare un 1 e si effettua il preprocessing
    sulla sottomatrice cosi' ottenuta.
    """

    if not original_matrix:
        original_matrix = deepcopy(matrix)
    if removed_cols:
        matrix.submatrix(removed_rows=removed_rows)
        matrix.submatrix(removed_cols=removed_cols)
        original_matrix.set_grey_rows(removed_cols[0])
    singletons, everywhere_ids = matrix.preprocessing()
    expr = generate_expression(singletons, everywhere_ids, original_matrix)
    if matrix.is_empty():
        return expr
    submatrices = matrix.partition()
    partitionable = True
    if not submatrices:
        submatrices = [matrix]
        partitionable = False
    prod_expr = ProdExpression()
    sum_expr = SumExpression()
    for submatrix in submatrices:
        if partitionable:
            result = sub_compute_mhs(deepcopy(submatrix), original_matrix)
            if result:
                prod_expr.add_operand(result)
        else:
            compl_cols = OrderedDict()
            while not submatrix.is_empty() and not submatrix.check_for_rows_without_1():
                # col_id = deepcopy(submatrix.cols.keys()).pop(0)
                col_id = submatrix.find_next_col(compl_cols)
                copy_original_matrix = deepcopy(original_matrix)
                if copy_original_matrix.check_hit_grey_rows(col_id):
                    submatrix.submatrix(removed_cols=[col_id])
                    continue
                hit_rows = submatrix.hit_rows(col_id)
                super_cols = submatrix.remove_super_cols(col_id)
                result = compute_mhs(deepcopy(submatrix), copy_original_matrix, [col_id] + super_cols, hit_rows)
                submatrix.submatrix(removed_cols=[col_id])
                if result and not result.is_empty():
                    sum_expr.add_operand(ProdExpression([AtomicElem(col_id), result]))
    result = sum_expr
    if partitionable:
        result = prod_expr
    if not expr:
        return result
    if not result.is_empty():
        incomplete_operand = expr.get_incomplete_operand()
        incomplete_operand.add_operand(result)
    return expr


def sub_compute_mhs(matrix, original_matrix):
    singletons, everywhere_ids = matrix.preprocessing()
    expr = generate_expression(singletons, everywhere_ids, original_matrix)
    sum_expr = SumExpression()
    compl_cols = OrderedDict()
    while not matrix.is_empty() and not matrix.check_for_rows_without_1():
        # max_col_ids = matrix.max_cols1()
        # if matrix.cols:
        # col_id = max_col_ids.pop(0)
        col_id = matrix.find_next_col(compl_cols)
        if original_matrix.check_hit_grey_rows(col_id):
            matrix.submatrix(removed_cols=[col_id])
            continue
        hit_rows = matrix.hit_rows(col_id)
        super_cols = matrix.remove_super_cols(col_id)
        result = compute_mhs(deepcopy(matrix), deepcopy(original_matrix), [col_id] + super_cols, hit_rows)
        matrix.submatrix(removed_cols=[col_id])
        if result and not result.is_empty():
            sum_expr.add_operand(ProdExpression([AtomicElem(col_id), result]))
    if not expr:
        return sum_expr
    if not sum_expr.is_empty():
        incomplete_operand = expr.get_incomplete_operand()
        incomplete_operand.add_operand(sum_expr)
    return expr


def generate_expression(singletons, everywhere_ids, original_matrix):
    """
    Genera un'espressione temporanea sulla base dei singoletti, degli id degli elementi appartenenti a tutti i mhs del
    contesto attuale e della mappa delle sostituzioni.
    """

    singletons, everywhere_ids = keep_valid_solutions(singletons, everywhere_ids, original_matrix)
    singletons = build_elements(singletons)
    everywhere_ids = build_elements(everywhere_ids)
    expr = None
    for i in range(len(singletons) - 1, -1, -1):
        prod = ProdExpression()
        if expr:
            prod.add_operand(expr)
        if everywhere_ids[i]:
            prod.add_operands(everywhere_ids[i])
        if singletons[i]:
            expr = SumExpression(singletons[i])
            if not prod.is_empty():
                expr.add_operand(prod)
        elif not prod.is_empty():
            expr = prod
    return expr

def keep_valid_solutions(singletons, everywhere_ids, original_matrix):
    for k in range(len(singletons)):
        i = 0
        s = singletons[k]
        while i < len(s):
            if deepcopy(original_matrix).check_hit_grey_rows(s[i]):
                s.pop(i)
            else:
                i += 1
        i = 0
        e = everywhere_ids[k]
        while i < len(e):
            if original_matrix.check_hit_grey_rows(e[i]):
                everywhere_ids[k] = []
                singletons = singletons[:k+1]
                everywhere_ids = everywhere_ids[:k+1]
                return singletons, everywhere_ids
            original_matrix.set_grey_rows(e[i])
            i += 1
    return singletons, everywhere_ids

def build_elements(elems):
    return [[AtomicElem(_id) for _id in elem] for elem in elems]

def create_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname + '/'


def show_progress(fname, partial, total):
    progress = int(round(100 * float(partial) / total))
    os.system('cls')
    print fname + ': progress: ' + str(progress) + '% (' + str(partial) + '/' + str(total) + ')'
